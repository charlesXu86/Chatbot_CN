define(['unit-js', 'role-js', 'dialog', 'common', 'knockout', 'knockout-mapping', 'jquery', 'jquery.ztree.excheck', 'jquery.ztree.exedit',
    'jquery.ztree.exhide','mCustomScrollbar'], function (unit, role, dialog, common, ko, mapping, $) {
    //mapping插件为单独的导出对象
    ko.mapping = mapping;
    var setting;

    /**
     * 移除节点鼠标悬浮操作界面
     * @param treeId
     * @param treeNode 当前节点
     */
    function removeHoverDom(treeId, treeNode) {
        $("#" + treeNode.tId + "_add").unbind().remove();
        $("#" + treeNode.tId + "_edit").unbind().remove();
        $("#" + treeNode.tId + "_remove").unbind().remove();
    }
    /**
     * 节点拖拽结束后重新绑定removeHover操作
     * @param event
     * @param treeId
     * @param treeNodes
     */
    function zTreeOnDrop(event, treeId, treeNodes) {
        for (var i = 0; i < treeNodes.length; i++) {
            var obj = treeNodes[i];
            $("#" + obj.tId).mouseleave(function () {
                (function (treeId, obj) {
                    removeHoverDom(treeId, obj);
                })(treeId, obj);
            });
        }
    }


    //查询人员树
    function loadHumanTree(that) {
        $.get('json/queryAllHumanTree.json', function (response) {
            if (common.dealResponse(response)) {
                $.fn.zTree.init($("#human-tree-list"), setting, response.data);
                //加载第一个部门节点信息
                var treeObj = common.tree.getTreeObj('human-tree-list');
                var nodes = treeObj.getNodes();
                if (nodes) {
                    treeObj.selectNode(nodes[0]);
                    removeHoverDom(null, nodes[0]);
                    that.formTitle('部门信息');
                    that.showUnitForm(true);
                    //加载部门基本信息
                    unit.loadUnitInfo(that, nodes[0].id.substring(1));
                }
            }
        });
    }


    //根据人员id查询人员本信息
    function loadHumanInfo(that, humanId) {
        $.get('json/queryHumanById.json', {humanId: humanId}, function (response) {
            if (common.dealResponse(response)) {
                that.humanInfo.humanpassword('');
                ko.mapping.fromJS(response.data, that.humanInfo);
            }
        });
    }

    //查询人员分配的岗位列表
    function loadRoleList(that, humanId) {
        $.post('role/queryAllRoleTree', function (response) {
            if (common.dealResponse(response)) {
                var nodes = response.data;
                if (nodes) {
                    $.fn.zTree.init($("#role-tree-list-human"), {
                            view: {
                                selectedMulti: true
                            },
                            check: {
                                enable: true
                            },
                            data: {
                                simpleData: {
                                    enable: true
                                }
                            },
                            edit: {
                                enable: false
                            },
                            callback: {
                                onCheck: function (event, treeId, treeNode) {
                                    var nums = that.allocated();
                                    //部门和岗位check时需要遍历其下的所有子节点
                                    var ids = [];
                                    if (treeNode.checked) {
                                        if (treeNode.id.indexOf('u') != -1 ) {
                                            common.tree.getChildren(ids, treeNode);
                                            for (var i = 0; i < ids.length; i++) {
                                                if (ids[i].indexOf('u') == -1 ) {
                                                    nums++;
                                                }
                                            }
                                            that.allocated(nums);
                                        } else {
                                            that.allocated(nums + 1);
                                        }
                                    } else {
                                        if (treeNode.id.indexOf('u') != -1 ) {
                                            common.tree.getChildren(ids, treeNode);
                                            for (var i = 0; i < ids.length; i++) {
                                                if (ids[i].indexOf('u') == -1 ) {
                                                    nums--;
                                                }
                                            }
                                            that.allocated(nums);
                                        } else {
                                            nums--;
                                        }
                                        that.allocated(nums - 1 >= 0 ? nums : 0);
                                    }
                                },
                                beforeCheck: function (treeId, treeNode) {
                                    //部门节点无法check
                                   /* if (treeNode.id.indexOf('u') != -1)
                                        return false;*/
                                }
                            }
                        },
                        nodes
                    )
                    ;
                    var treeObj = common.tree.getTreeObj('role-tree-list-human');
                    //设置当前选中的岗位
                    $.post('human/queryRolesByHumanId', {humanId: humanId}, function (response) {
                        if (common.dealResponse(response)) {
                            var selectedRoles = response.data;
                            that.allocated(selectedRoles.length);
                            //查找所有的岗位节点
                            treeObj.getNodesByFilter(function (node) {
                                //排除部门节点
                                if (node.id.indexOf('u') == -1 && selectedRoles) {
                                    for (var k = 0; k < selectedRoles.length; k++) {
                                        var s = selectedRoles[k];
                                        if (s.roleid == node.id) {
                                            treeObj.checkNode(node, true, true);
                                            break;
                                        }
                                    }
                                }
                            });
                            ko.mapping.fromJS(response.data, that.roleList);
                        }
                    });
                }
            }
        });
    }

    //新增人员
    function addHuman(treeNode, humanInfo, that) {
        $.ajax({
            url: 'human/addHuman',
            data: JSON.stringify(humanInfo),
            contentType: "application/json; charset=utf-8",
            dataType: "json",
            method: "post",
            success: function (response) {
                if (common.dealResponse(response)) {
                    var zTree = common.tree.getTreeObj('human-tree-list');
                    zTree.addNodes(treeNode, {
                        id: "" + response.data.humanid,
                        pId: "r" + humanInfo.roleid,
                        name: response.data.humanname,
                        icon: 'image/icon/human.png'
                    });

                    ko.mapping.fromJS(response.data, that.humanInfo);
                    //show the human form
                    that.isUnitNode(false);
                    that.showHumanForm(true);
                    that.showUnitForm(false);
                    that.showRoleForm(false);
                    //获取新加的节点
                    var newNode = zTree.getNodesByParam("id", response.data.humanid, treeNode);
                    //选中新增的节点
                    if (newNode)
                        zTree.selectNode(newNode[0]);
                    dialog.tips({
                        message: '新增人员成功',
                        type: 'success'
                    });
                }
            }
        });
    }

    //删除岗位
    function delHuman(humanId, that) {
        $.post('human/delHuman', {humanId: humanId}, function (response) {
            if (common.dealResponse(response)) {
                dialog.tips({
                    message: '删除人员成功',
                    type: 'success'
                });
                that.showHumanForm(false);
            }
        });
    }

    //初始化ko绑定
    function initHumanInfo(that) {
        //绑定岗位基本信息
        that.humanInfo = ko.mapping.fromJS({
            humanid: '',
            humancode: '',
            unitid: '',
            humanname: '',
            displayorder: '',
            humandescription: '',
            macaddress: '',
            telmobile: '',
            dutyid: '',
            humanpassword: '',
            dutyList:common.dic.dutyData
        });
    }

    function human() {
        var that = this;
        //绑定岗位
        this.roleList = ko.mapping.fromJS([]);
        this.isUnitNode = ko.observable(true);
        this.showHumanForm = ko.observable(true);
        this.showUnitForm = ko.observable(false);
        this.showRoleForm = ko.observable(false);
        this.formTitle = ko.observable('');
        this.filterRoles = ko.observable(false);
        //人员系统功能权限列表
        this.otherResList = ko.observableArray();
        //已分配的平台菜单权限数量
        this.navMenuRes = ko.observable(0);
        this.appMenuRes = ko.observable(0);
        this.otherRes = ko.observable(0);
        //人员关联的岗位过滤
        this.filterRoles.subscribe(function (newValue) {
            var treeObj = common.tree.getTreeObj('role-tree-list-human');
            if (newValue) {
                if (treeObj) {
                    treeObj.getNodesByFilter(function (node) {
                        //未选中的岗位节点隐藏
                        if (node.id.indexOf('u') == -1 && !node.checked) {
                            treeObj.hideNode(node);
                        }
                    });
                }
            } else {
                if (treeObj) {
                    treeObj.getNodesByFilter(function (node) {
                        if (node.isHidden) {
                            treeObj.showNode(node);
                        }
                    });
                }
            }
        });
        //已分配的岗位数
        this.allocated = ko.observable('');
        initHumanInfo(that);
        //页面加载前初始化操作
        this.init = function () {
            setting = {
                view: {
                    addHoverDom: function (treeId, treeNode) {
                        //only role node can add human
                        if (treeNode.id.indexOf('r') == -1)
                            return false;
                        //岗位的父节点是部门节点
                        var parentNode = treeNode.getParentNode();
                        var roleid = treeNode.id.substring(1);
                        var sObj = $("#" + treeNode.tId + "_span");
                        if (treeNode.editNameFlag || $("#" + treeNode.tId + "_add").length > 0) return;
                        var addStr = "<span class='button add' id='" + treeNode.tId
                            + "_add' title='新增' onfocus='this.blur();'></span>";
                        sObj.after(addStr);
                        var btn = $("#" + treeNode.tId + "_add");
                        if (btn) btn.bind("click", function () {
                            var human = {
                                humanname: '新增人员',
                                humandescription: '新增人员描述',
                                roleid: roleid,
                                unitid: parentNode.id.substring(1)
                            };
                            addHuman(treeNode, human, that);
                            return false;
                        });
                    },
                    removeHoverDom: removeHoverDom,
                    selectedMulti: false
                },
                check: {
                    enable: false
                },
                data: {
                    simpleData: {
                        enable: true
                    }
                },
                edit: {
                    enable: true,
                    deleteConfirmText: '是否删除该人员?'
                },
                callback: {
                    onDrop: zTreeOnDrop,
                    onRename: function zTreeOnRename(event, treeId, treeNode, isCancel) {
                        //没有取消重命名操作
                        if (!isCancel) {
                            //更新岗位基本信息
                            that.humanInfo.rolename(treeNode.name);
                        }
                    },
                    onRemove: function (event, treeId, treeNode) {
                        delHuman(treeNode.id, that);
                    },
                    beforeRename: function (treeId, treeNode, newName, isCancel) {
                        if ((treeNode.id.indexOf('u') != -1 || treeNode.id.indexOf('r') != -1) && !isCancel) {
                            dialog.errorTips('只能修改人员名称');
                            common.tree.getTreeObj('human-tree-list').cancelEditName(treeNode.name);
                        }
                        return true;
                    },
                    beforeRemove: function (treeId, treeNode) {
                        if (treeNode.id.indexOf('u') != -1 || treeNode.id.indexOf('r') != -1) {
                            dialog.errorTips('只能删除人员节点');
                            return false;
                        }
                        return true;
                    },
                    onClick: function (event, treeId, treeNode) {
                        //机构节点
                        if (treeNode.id.indexOf('u') != -1) {
                            //show role editor
                            that.showRoleForm(false);
                            that.showUnitForm(true);
                            that.showHumanForm(false);
                            that.isUnitNode(true);
                            that.formTitle('部门信息');
                            //加载机构信息
                            unit.loadUnitInfo(that, treeNode.id.substring(1));
                        } else if (treeNode.id.indexOf('r') != -1) {//岗位节点
                            that.showRoleForm(true);
                            that.showUnitForm(false);
                            that.showHumanForm(false);
                            that.isUnitNode(true);
                            that.formTitle('岗位信息');
                            //加载岗位信息
                            role.loadRoleInfo(that, treeNode.id.substring(1));
                        } else {//人员节点
                            that.formTitle('编辑人员信息');
                            //show role editor
                            that.showHumanForm(true);
                            that.showRoleForm(false);
                            that.showUnitForm(false);
                            that.isUnitNode(false);
                            //加载岗位信息
                            loadHumanInfo(that, treeNode.id);
                            //加载人员
                            loadRoleList(that, treeNode.id);
                            //加载人员权限
                            that.loadAuthTree(treeNode.id);
                        }
                    }
                }
            };
            //初始化机构
            unit.initUnitInfo(that);
            //初始化岗位
            role.initRoleInfo(that);
        };

        //页面渲染完毕
        this.afterRender = function (element) {
            initUI(this);
        };
        //更新人员信息
        this.updateHumanInfo = function () {
            var humanInfo = ko.mapping.toJS(this.humanInfo);
            $.ajax({
                url: 'human/updateHuman',
                data: JSON.stringify(humanInfo),
                contentType: "application/json; charset=utf-8",
                dataType: "json",
                method: "post",
                success: function (response) {
                    if (common.dealResponse(response)) {
                        //modify node name
                        common.tree.updateNode('human-tree-list', humanInfo.humanname);
                        dialog.tips({
                            message: '更新人员信息成功',
                            type: 'success'
                        });
                    }
                }
            });
        };
        //重置人员信息
        this.resetHumanInfo = function () {
            loadHumanInfo(this, this.humanInfo.humanid())
        };
        //删除岗位
        this.delHumanInfo = function () {
            var currNode = common.tree.getSelectedNode('human-tree-list');
            var humanId = this.humanInfo.humanid();
            if (!humanId || !currNode) {
                dialog.tips({
                    message: '请选择有效的岗位节点进行删除',
                    type: 'danger'
                });
                return;
            }
            common.tree.getTreeObj('human-tree-list').removeNode(currNode, true);
        };

        //更新岗位信息
        this.allocateRoles = function () {
            var treeObj = common.tree.getTreeObj('role-tree-list-human');
            var selectedRoles = treeObj.getNodesByFilter(function (node) {
                return node.id.indexOf('u') == -1 && node.checked;
            });
            if (!selectedRoles || selectedRoles.length == 0) {
                dialog.errorTips('请选配置有效的岗位信息');
                return;
            }
            var roleIds = [];
            for (var i = 0; i < selectedRoles.length; i++) {
                var obj = selectedRoles[i];
                roleIds.push(obj.id);
            }
            $.post('human/allocateRoles', {
                roleIds: roleIds.join(","),
                humanId: that.humanInfo.humanid()
            }, function (response) {
                if (common.dealResponse(response))
                    dialog.successTips('岗位配置成功');
            });
        };
        //重置岗位
        this.resetHumanRoles = function () {
            loadRoleList(that, this.humanInfo.humanid());
        };
        //加载人员权限
        this.loadAuthTree = function (humanId) {
            $.get('json/queryResourceTree.json', function (response) {
                if (common.dealResponse(response)) {
                    var resources = response.data;
                    var navMenu = [];
                    var appMenu = [];
                    that.otherResList.removeAll();
                    for (var i = 0; i < resources.length; i++) {
                        var obj = resources[i];
                        if (obj.type == 1)
                            navMenu.push(obj);
                        else if (obj.type == 3)
                            appMenu.push(obj);
                        else {
                            obj.checked = false;
                            var o = ko.mapping.fromJS(obj);
                            that.otherResList.push(o);
                        }
                        //更新其他功能权限
                    }
                    $.fn.zTree.init($("#human-resource-tree-list"), {
                        view: {
                            selectedMulti: false
                        },
                        check: {
                            enable: true,
                            chkStyle: "checkbox",
                        },
                        data: {
                            simpleData: {
                                enable: true
                            }
                        },
                        edit: {
                            enable: false
                        },
                        callback: {
                            beforeCheck: function (treeId, treeNode) {
                                return false;
                            }
                        }
                    }, navMenu);
                    $.fn.zTree.init($("#human-app-tree-list"), {
                        view: {
                            selectedMulti: false
                        },
                        check: {
                            enable: true,
                            chkStyle: "checkbox",
                        },
                        data: {
                            simpleData: {
                                enable: true
                            }
                        },
                        edit: {
                            enable: false
                        },
                        callback: {
                            beforeCheck: function (treeId, treeNode) {
                                return false;
                            }
                        }
                    }, appMenu);
                    //已分配权限check
                    $.get('json/queryResourceByHumanId.json', {humanId: humanId}, function (response) {
                        if (common.dealResponse(response)) {
                            var resourceList = response.data;
                            if (!resourceList || resourceList.length == 0) {
                                that.navMenuRes(0);
                                that.otherRes(0);
                                return;
                            }
                            var treeObj = common.tree.getTreeObj('human-resource-tree-list');
                            //平台菜单选中
                            var navR = appR = otherR = 0;
                            treeObj.getNodesByFilter(function (node) {
                                for (var k = 0; k < resourceList.length; k++) {
                                    var s = resourceList[k];
                                    if (s.resourceid == node.id) {
                                        treeObj.checkNode(node, true, false);
                                        navR++;
                                    }
                                }
                            });
                            //应用菜单选中
                            treeObj = common.tree.getTreeObj('human-app-tree-list');
                            treeObj.getNodesByFilter(function (node) {
                                for (var k = 0; k < resourceList.length; k++) {
                                    var s = resourceList[k];
                                    if (s.resourceid == node.id) {
                                        treeObj.checkNode(node, true, false);
                                        appR++;
                                    }
                                }
                            });
                            //其他权限勾选
                            var other = that.otherResList();
                            for (var i = 0; i < other.length; i++) {
                                for (var k = 0; k < resourceList.length; k++) {
                                    var s = resourceList[k];
                                    if (s.resourceid == other[i].id()) {
                                        other[i].checked(true);
                                        otherR++;
                                    }
                                }
                            }
                            that.navMenuRes(navR);
                            that.appMenuRes(appR);
                            that.otherRes(otherR);
                        }
                    });
                }
            });
        };
    }

    //构建系统界面
    var initUI = function (that) {
        //获取人员树
        loadHumanTree(that);
        autoHeight();
        //解决树节点单击操作按钮不消失
        $("#human-tree-list").mouseleave(function () {
            removeHoverDom('', common.tree.getSelectedNode('human-tree-list'));
        });
    };

    //岗位树高度自适应
    function autoHeight() {
        var windowHeight = $(window).height();
        var contentHeaderHeight = $(".content-tabs").height();
        var mainHeaderHeight = $(".main-header").height();
        var mainFooterHeight = $(".main-footer").height();
        var iheight = windowHeight - mainHeaderHeight - contentHeaderHeight - mainFooterHeight;
        $("#humanListBox").height(iheight);
        $("#roleList").height(iheight);
        $("#humanListBox").mCustomScrollbar({
            theme:"light-thin"
        });
        $("#roleList").mCustomScrollbar({
            theme:"light-thin"
        });
    }

    $(window).resize(function () {
        autoHeight();
    });
    var human = new human();
    //export
    return human;
});
