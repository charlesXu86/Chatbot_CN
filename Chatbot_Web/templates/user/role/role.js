define(['unit-js', 'dialog', 'common', 'knockout', 'knockout-mapping', 'jquery', 'jquery.ztree.excheck', 'jquery.ztree.exedit',
    'jquery.ztree.exhide','mCustomScrollbar'], function (unit, dialog, common, ko, mapping, $) {
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


    //查询岗位数据
    function loadRoleTree(that, fn) {
        $.get('json/queryAllRoleTree.json', function (response) {
            if (common.dealResponse(response)) {
                if (fn) fn(response);
            }
        });
    }


    //根据岗位id查询岗位基本信息
    function loadRoleInfo(that, roleId) {
        $.get('json/queryRoleById.json', {roleId: roleId}, function (response) {
            if (common.dealResponse(response)) {
                ko.mapping.fromJS(response.data, that.roleInfo);
            }
        });
    }

    //查询岗位分配的人员列表
    function loadHumanList(that, roleId) {
        $.post('role/queryHumansByRoleId', {roleId: roleId}, function (response) {
            if (common.dealResponse(response)) {
                var humanData = response.data;
                if (humanData) {
                    that.allocated(humanData.length);
                    ko.mapping.fromJS(humanData, that.humanList);
                }
            }
        });
    }

    //新增岗位
    function addRole(treeNode, roleInfo, that) {
        $.ajax({
            url: 'role/addRole',
            data: JSON.stringify(roleInfo),
            contentType: "application/json; charset=utf-8",
            dataType: "json",
            method: "post",
            success: function (response) {
                if (common.dealResponse(response)) {
                    var zTree = common.tree.getTreeObj('role-tree-list');
                    zTree.addNodes(treeNode, {
                        id: "" + response.data.roleid,
                        pId: "u" + roleInfo.unitid,
                        name: roleInfo.rolename,
                        icon: 'image/icon/role.png'
                    });

                    ko.mapping.fromJS(response.data, that.roleInfo);
                    //show the role form
                    that.isUnitNode(false);
                    //获取新加的节点
                    var newNode = zTree.getNodesByParam("id", response.data.roleid, treeNode);
                    //选中新增的节点
                    if (newNode)
                        zTree.selectNode(newNode[0]);
                    dialog.tips({
                        message: '新增岗位成功',
                        type: 'success'
                    });
                }
            }
        });
    }

    //删除岗位
    function delRole(roleId, that) {
        $.post('role/delRole', {roleId: roleId}, function (response) {
            if (common.dealResponse(response)) {
                dialog.tips({
                    message: '删除岗位成功',
                    type: 'success'
                });
                that.showRoleForm(false);
            }
        });
    }

    function initRoleInfo(that) {
        //绑定岗位基本信息
        that.roleInfo = ko.mapping.fromJS({
            roleid: '',
            unitid: '',
            rolename: '',
            displayorder: '',
            roledescription: ''
        });
    }

    function role() {
        var that = this;
        //绑定岗位
        this.humanList = ko.mapping.fromJS([]);
        this.isUnitNode = ko.observable(true);
        this.showRoleForm = ko.observable(true);
        this.formTitle = ko.observable('');
        //岗位关联的人员数量
        this.allocated = ko.observable('');
        //非平台菜单功能权限
        this.otherResList = ko.observableArray();
        initRoleInfo(that);
        //页面加载前初始化操作
        this.init = function () {
            setting = {
                view: {
                    addHoverDom: function (treeId, treeNode) {
                        //only unit node can add role
                        if (treeNode.id.indexOf('u') == -1)
                            return false;
                        var unitId = treeNode.id.substring(1);
                        var sObj = $("#" + treeNode.tId + "_span");
                        if (treeNode.editNameFlag || $("#" + treeNode.tId + "_add").length > 0) return;
                        var addStr = "<span class='button add' id='" + treeNode.tId
                            + "_add' title='新增' onfocus='this.blur();'></span>";
                        sObj.after(addStr);
                        var btn = $("#" + treeNode.tId + "_add");
                        if (btn) btn.bind("click", function () {
                            var role = {
                                rolename: '新增岗位',
                                roledescription: '新增岗位描述',
                                unitid: unitId
                            };
                            addRole(treeNode, role, that);
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
                    deleteConfirmText: '是否删除该岗位?'
                },
                callback: {
                    onDrop: zTreeOnDrop,
                    onRename: function (event, treeId, treeNode, isCancel) {
                        //没有取消重命名操作
                        if (!isCancel) {
                            //更新岗位基本信息
                            that.roleInfo.rolename(treeNode.name);
                        }
                    },
                    onRemove: function (event, treeId, treeNode) {
                        delRole(treeNode.id, that);
                    },
                    beforeRename: function (treeId, treeNode, newName, isCancel) {
                        if (treeNode.id.indexOf('u') != -1 && !isCancel) {
                            dialog.errorTips('只能修改岗位名称');
                            common.tree.getTreeObj('role-tree-list').cancelEditName(treeNode.name);
                        }
                        return true;
                    },
                    beforeRemove: function (treeId, treeNode) {
                        if (treeNode.id.indexOf('u') != -1) {
                            dialog.errorTips('只能删除岗位节点');
                            return false;
                        }
                        return true;
                    },
                    onClick: function (event, treeId, treeNode) {
                        //机构节点
                        if (treeNode.id.indexOf('u') != -1) {
                            //show role editor
                            that.showRoleForm(false);
                            that.isUnitNode(true);
                            that.formTitle('部门信息');
                            //加载机构信息
                            unit.loadUnitInfo(that, treeNode.id.substring(1));
                        } else {//岗位节点
                            that.formTitle('编辑岗位信息');
                            //show role editor
                            that.showRoleForm(true);
                            that.isUnitNode(false);
                            //加载岗位信息
                            loadRoleInfo(that, treeNode.id);
                            //加载人员
                            loadHumanList(that, treeNode.id);
                            //加载权限列表
                            that.loadAuthTree(treeNode.id);
                        }
                    }
                }
            };
            //初始化机构
            unit.initUnitInfo(that);
        };
        //重置岗位权限
        this.resetRoleResource = function (role) {
            this.loadAuthTree(role.roleInfo.roleid());
        };
        //保存岗位权限
        this.saveResources = function (role) {
            var treeObj = common.tree.getTreeObj('role-resource-tree-list');
            var selectedResource = treeObj.getNodesByFilter(function (node) {
                return node.checked;
            });

            treeObj = common.tree.getTreeObj('role-app-tree-list');
            var appResources = treeObj.getNodesByFilter(function (node) {
                return node.checked;
            });
            selectedResource = selectedResource.concat(appResources);
            var resourceIds = [];
            //菜单导航权限
            for (var i = 0; i < selectedResource.length; i++) {
                var obj = selectedResource[i];
                resourceIds.push(obj.id);
            }
            //其他权限
            var otherList = that.otherResList();
            if (otherList && otherList.length > 0) {
                for (var i = 0; i < otherList.length; i++) {
                    var o = otherList[i];
                    //只选择已勾选的项
                    if (o.checked())
                        resourceIds.push(o.id());
                }
            }
            $.post('auth/updateRoleResources', {
                resourceIds: resourceIds.join(","),
                roleId: role.roleInfo.roleid()
            }, function (response) {
                if (common.dealResponse(response))
                    dialog.successTips('权限配置成功');
            });
        };
        //加载平台菜单树
        this.loadAuthTree = function (roleId) {
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
                        else if(obj.type == 3)
                            appMenu.push(obj);
                        else {
                            obj.checked = false;
                            var o = ko.mapping.fromJS(obj);
                            that.otherResList.push(o);
                        }
                        //更新其他功能权限
                    }
                    $.fn.zTree.init($("#role-resource-tree-list"), {
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
                        }
                    }, navMenu);
                    $.fn.zTree.init($("#role-app-tree-list"), {
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
                        }
                    }, appMenu);
                    //已分配权限check
                    $.get('json/queryResourceByRoleId.json', {roleId: roleId}, function (response) {
                        if (common.dealResponse(response)) {
                            var resourceList = response.data;
                            if (!resourceList || resourceList.length == 0)
                                return;
                            var treeObj = common.tree.getTreeObj('role-resource-tree-list');
                            //平台菜单选中
                            treeObj.getNodesByFilter(function (node) {
                                for (var k = 0; k < resourceList.length; k++) {
                                    var s = resourceList[k];
                                    if (s.resourceid == node.id) {
                                        treeObj.checkNode(node, true, false);
                                    }
                                }
                            });
                            treeObj = common.tree.getTreeObj('role-app-tree-list');
                            //应用菜单选中
                            treeObj.getNodesByFilter(function (node) {
                                for (var k = 0; k < resourceList.length; k++) {
                                    var s = resourceList[k];
                                    if (s.resourceid == node.id) {
                                        treeObj.checkNode(node, true, false);
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
                                    }
                                }
                            }
                        }
                    });
                }
            });
        };
        //页面渲染完毕
        this.afterRender = function (element) {
            initUI(this);
        };
        //更新岗位信息
        this.updateRoleInfo = function () {
            var roleInfo = ko.mapping.toJS(this.roleInfo);
            $.ajax({
                url: 'role/updateRole',
                data: JSON.stringify(roleInfo),
                contentType: "application/json; charset=utf-8",
                dataType: "json",
                method: "post",
                success: function (response) {
                    if (common.dealResponse(response)) {
                        //modify node name
                        common.tree.updateNode('role-tree-list', roleInfo.rolename,response.data);
                        dialog.tips({
                            message: '更新岗位信息成功',
                            type: 'success'
                        });
                    }
                }
            });
        };
        //重置岗位信息
        this.resetRoleInfo = function () {
            loadRoleInfo(this, this.roleInfo.roleid())
        };
        //删除岗位
        this.delRoleInfo = function () {
            var currNode = common.tree.getSelectedNode('role-tree-list');
            var roleId = this.roleInfo.roleid();
            if (!roleId || !currNode) {
                dialog.tips({
                    message: '请选择有效的岗位节点进行删除',
                    type: 'danger'
                });
                return;
            }
            common.tree.getTreeObj('role-tree-list').removeNode(currNode, true);
        }

    }

    //构建系统界面
    var initUI = function (that) {
        //获取岗位列表
        loadRoleTree(that, function (response) {
            $.fn.zTree.init($("#role-tree-list"), setting, response.data);
            //加载第一个单位节点信息
            var treeObj = common.tree.getTreeObj('role-tree-list');
            var nodes = treeObj.getNodes();
            if (nodes) {
                treeObj.selectNode(nodes[0]);
                removeHoverDom(null, nodes[0]);
                that.formTitle('部门信息');
                //加载单位基本信息
                unit.loadUnitInfo(that, nodes[0].id.substring(1));
            }
        });
        autoHeight();
        //解决树节点单击操作按钮不消失
        $("#role-tree-list").mouseleave(function () {
            removeHoverDom('', common.tree.getSelectedNode('role-tree-list'));
        });
    };

    //岗位树高度自适应
    function autoHeight() {
        var tabHeight = $(".nav.nav-tabs").height();
        var contentHeaderHeight = $(".content-tabs").height();
        var windowHeight = $(window).height();
        var mainHeaderHeight = $(".main-header").height();
        var mainFooterHeight = $(".main-footer").height();
        var iheight = windowHeight - mainHeaderHeight - contentHeaderHeight - mainFooterHeight;
        $("#roleListBox").height(iheight);
        $("#roleHumanList").height(iheight - tabHeight);
        //$("#sysMenuTree").height(iheight - tabHeight);
        $("#roleListBox").mCustomScrollbar({
            theme:"light-thin"
        });
        $("#roleHumanList").mCustomScrollbar({
            theme:"light-thin"
        });
    }

    $(window).resize(function () {
        autoHeight();
    });
    //export
    var role = new role();
    role.loadRoleInfo = loadRoleInfo;
    role.initRoleInfo = initRoleInfo;
    role.loadRoleTree = loadRoleTree;
    return role;
})
;
