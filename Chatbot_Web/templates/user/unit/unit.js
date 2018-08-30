define(['dialog', 'common', 'knockout', 'knockout-mapping', 'jquery', /* 'jquery.ztree.excheck',*/ 'jquery.ztree.exedit',
    'jquery.ztree.exhide','mCustomScrollbar'], function (dialog, common, ko, mapping, $) {
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


    //查询部门数据
    function loadUnitTree(that) {
        $.get('json/queryAllUnitTree.json', function (response) {
            if (common.dealResponse(response)) {
                $.fn.zTree.init($("#unit-tree-list"), setting, response.data);
                var treeObj = common.tree.getTreeObj('unit-tree-list');
                //默认第一个部门节点选中
                var nodes = treeObj.getNodes();
                if (nodes) {
                    treeObj.selectNode(nodes[0]);
                    removeHoverDom(null, nodes[0]);
                    //加载单位基本信息
                    loadUnitInfo(that, nodes[0].id);
                }
            }
        });
    }

    //查询岗位
    function loadRoles(that, unitId) {
        $.get('json/queryRolesByUnitId.json', {unitId: unitId}, function (response) {
            if (common.dealResponse(response))
                ko.mapping.fromJS(response.data, that.roleList);
        });
    }

    //根据部门id查询部门基本信息
    function loadUnitInfo(that, unitId) {
        $.get('json/queryUnitByUnitId.json', {unitId: unitId}, function (response) {
            if (common.dealResponse(response)) {
                ko.mapping.fromJS(response.data, that.unitInfo);
            }
        });
    }

    //新增部门
    function addUnit(treeNode, unitInfo, that) {
        $.ajax({
            url: 'unit/addUnit',
            data: JSON.stringify(unitInfo),
            contentType: "application/json; charset=utf-8",
            dataType: "json",
            method: "post",
            success: function (response) {
                if (common.dealResponse(response)) {
                    var zTree = common.tree.getTreeObj('unit-tree-list');
                    zTree.addNodes(treeNode, {
                        id: response.data.unitid,
                        pId: unitInfo.seniorunitid,
                        name: unitInfo.unitname,
                        icon: 'image/icon/unit.png'
                    });
                    ko.mapping.fromJS(response.data, that.unitInfo);
                    //获取新加的节点
                    var newNode = zTree.getNodesByParam("id", response.data.unitid, treeNode);
                    //选中新增的节点
                    if(newNode)
                        zTree.selectNode(newNode[0]);
                    dialog.tips({
                        message: '新增部门成功',
                        type: 'success'
                    });
                }
            }
        });
    }

    //删除部门
    function delUnit(unitId, that) {
        $.post('unit/delUnit', {unitId: unitId}, function (response) {
            if (common.dealResponse(response)) {
                dialog.tips({
                    message: '删除部门成功',
                    type: 'success'
                });
                that.showUnitForm(false);
            }
        });
    }

    function clearUnitInfo(that) {
        ko.mapping.fromJS({
            unitid: '',
            unitname: '',
            createdate: '',
            displayorder: '',
            unitdescription: ''
        }, that.unitInfo);
    }

    function initUnitInfo(that) {
        //绑定部门基本信息
        that.unitInfo = ko.mapping.fromJS({
            unitid: '',
            unitname: '',
            createdate: '',
            displayorder: '',
            unitdescription: '',
            cantonid: ''
        });
    }

    function unit() {
        var that = this;
        //绑定岗位
        this.roleList = ko.mapping.fromJS([]);
        this.showUnitForm = ko.observable(true);
        initUnitInfo(that);
        //页面加载前初始化操作
        this.init = function () {
            setting = {
                view: {
                    addHoverDom: function (treeId, treeNode) {
                        var sObj = $("#" + treeNode.tId + "_span");
                        if (treeNode.editNameFlag || $("#" + treeNode.tId + "_add").length > 0) return;
                        var addStr = "<span class='button add' id='" + treeNode.tId
                            + "_add' title='新增' onfocus='this.blur();'></span>";
                        sObj.after(addStr);
                        var btn = $("#" + treeNode.tId + "_add");
                        if (btn) btn.bind("click", function () {
                            var unit = {
                                unitname: '新增部门',
                                unitdescription: '新增部门描述',
                                seniorunitid: treeNode.id
                            };
                            addUnit(treeNode, unit, that);
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
                    deleteConfirmText: '是否删除该部门?'
                },
                callback: {
                    onDrop: zTreeOnDrop,
                    onRename: function zTreeOnRename(event, treeId, treeNode, isCancel) {
                        //没有取消重命名操作
                        if (!isCancel) {
                            //更新部门基本信息
                            that.unitInfo.unitname(treeNode.name);
                        }
                    }
                    ,
                    onRemove: function (event, treeId, treeNode) {
                        delUnit(treeNode.id, that);
                    },
                    beforeRemove: function (treeId, treeNode) {
                        if (treeNode.isParent) {
                            dialog.errorTips('该部门关联子部门，不能删除');
                            return false;
                        }
                        return true;
                    },
                    onClick: function (event, treeId, treeNode) {
                        //unit eidtor visible now
                        that.showUnitForm(true);
                        //加载部门信息
                        loadUnitInfo(that, treeNode.id);
                        //加载岗位
                        loadRoles(that, treeNode.id);
                    }
                }
            };
        };

        //页面渲染完毕
        this.afterRender = function (element) {
            initUI(this);
        };
        //更新部门信息
        this.updateUnitInfo = function () {
            var unitInfo = ko.mapping.toJS(this.unitInfo);
            $.ajax({
                url: 'unit/updateUnit',
                data: JSON.stringify(unitInfo),
                contentType: "application/json; charset=utf-8",
                dataType: "json",
                method: "post",
                success: function (response) {
                    if (common.dealResponse(response)) {
                        //modify node name
                        common.tree.updateNode('unit-tree-list', unitInfo.unitname);
                        dialog.tips({
                            message: '更新部门信息成功',
                            type: 'success'
                        });
                    }
                }
            });
        };
        //重置部门信息
        this.resetUnitInfo = function () {
            loadUnitInfo(this, this.unitInfo.unitid())
        };
        //删除部门
        this.delUnitInfo = function () {
            var currNode = common.tree.getSelectedNode('unit-tree-list');
            var unitId = this.unitInfo.unitid();
            if (!unitId || !currNode) {
                dialog.tips({
                    message: '请选择有效的部门节点进行删除',
                    type: 'danger'
                });
                return;
            }
            common.tree.getTreeObj('unit-tree-list').removeNode(currNode, true);
        }

    }

    //构建系统界面
    var initUI = function (that) {
        //获取部门列表
        loadUnitTree(that);
        autoHeight();
        //解决树节点单击操作按钮不消失
        $("#unit-tree-list").mouseleave(function () {
            var node = common.tree.getSelectedNode('unit-tree-list');
            removeHoverDom('', node);
        });
    };

    //部门树高度自适应
    function autoHeight() {
        var tabHeight = $(".nav.nav-tabs").height();
        var contentHeaderHeight = $(".content-tabs").height();
        var windowHeight = $(window).height();
        var mainHeaderHeight = $(".main-header").height();
        var mainFooterHeight = $(".main-footer").height();
        var iheight = windowHeight - mainHeaderHeight - contentHeaderHeight -mainFooterHeight;
        $("#unitListBox").height(iheight);
        $("#unitRoleList").height(iheight- tabHeight);
        $("#unitListBox").mCustomScrollbar({
            theme:"light-thin"
        });
        $("#unitRoleList").mCustomScrollbar({
            theme:"light-thin"
        });
    }

    $(window).resize(function () {
        autoHeight();
    });
    //export
    var unit = new unit();
    unit.loadUnitInfo = loadUnitInfo;
    unit.initUnitInfo = initUnitInfo;
    return unit;
})
;
