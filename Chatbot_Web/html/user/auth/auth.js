define(['role-js', 'dialog', 'common', 'knockout', 'knockout-mapping', 'jquery', 'jquery.ztree.excheck', 'jquery.treegrid.extension','mCustomScrollbar'],
    function (role, dialog, common, ko, mapping, $) {
        //mapping插件为单独的导出对象
        ko.mapping = mapping;

        function auth() {
            var that = this;
            //页面加载前初始化操作
            this.init = function () {
                this.popTitle = ko.observable('新增权限');
                this.showAuthTree = ko.observable(false);
                this.parentResName = ko.observable('');
                //权限已分配岗位数
                this.allocated = ko.observable(0);
                this.typeList = ko.observableArray(common.dic.resourceTypeData);
                this.initAuthInfo();
            };
            this.initAuthInfo = function () {
                that.authInfo = ko.mapping.fromJS({
                    resourceid: '',
                    name: '',
                    resIco: '',
                    routeUrl: '',
                    hrefUrl: '',
                    resurl: '',
                    type: '',
                    displayorder: '',
                    modifyTime: '',
                    parentid: ''
                });
                that.authInfo.type(common.dic.resourceTypeData[0].typeid);
            };
            this.clearAuthInfo = function () {
                ko.mapping.fromJS({
                    resourceid: '',
                    name: '',
                    resIco: '',
                    routeUrl: '',
                    hrefUrl: '',
                    resurl: '',
                    type: '',
                    displayorder: '',
                    modifyTime: '',
                    parentid: ''
                }, that.authInfo);
                that.parentResName('');
                that.authInfo.type(common.dic.resourceTypeData[0].typeid);
            };
            //新增权限资源
            this.addResource = function () {
                //保存权限
                var authInfo = ko.mapping.toJS(that.authInfo);
                $.ajax({
                    url: 'auth/addResource',
                    data: JSON.stringify(authInfo),
                    contentType: "application/json; charset=utf-8",
                    dataType: "json",
                    method: "post",
                    success: function (response) {
                        if (common.dealResponse(response)) {
                            $("#modal-add-auth").modal('hide');
                            dialog.successTips('新增权限资源成功...');
                            that.treeTable = that.treeTable.treegridData('reDraw');
                        }
                    }
                });
            };
            //父权限选择树显示状态
            this.triggerSelectTree = function () {
                this.showAuthTree(!this.showAuthTree());
            };
            //打开新增弹窗
            this.openAddAuthWin = function () {
                that.clearAuthInfo();
                that.popTitle('新增权限');
                var node = that.treeTable.treegridData('getSelectedNode');
                //如果选了数据，则直接把它作为父节点
                if (node && node.resourceid) {
                    that.parentResName(node.name);
                    that.authInfo.parentid(node.resourceid);
                }
            };
            //加载权限关联的岗位数据
            this.loadResourceRoles = function (resourceId) {
                $.post('auth/queryRolesByResourceId', {resourceId: resourceId}, function (response) {
                    if (common.dealResponse(response)) {
                        var treeObj = common.tree.getTreeObj('role-tree-list-auth');
                        that.allocated(response.data.length);
                        //平台菜单选中
                        treeObj.getNodesByFilter(function (node) {
                            for (var k = 0; k < response.data.length; k++) {
                                var s = response.data[k];
                                if (s == node.id) {
                                    treeObj.checkNode(node, true, false);
                                }
                            }
                        });
                    }
                });
            };
            this.updateResourceRoles = function () {
                var node = that.currNode;
                if (!node) {
                    dialog.errorTips('请选择权限数据行行进行操作');
                    return;
                }
                var treeObj = common.tree.getTreeObj('role-tree-list-auth');
                var selectedRoles = treeObj.getNodesByFilter(function (node) {
                    return node.checked;
                });
                var roleIds = [];
                //菜单导航权限
                for (var i = 0; i < selectedRoles.length; i++) {
                    var obj = selectedRoles[i];
                    roleIds.push(obj.id);
                }
                $.post('auth/updateResourceRoles', {
                    roleIds: roleIds.join(","),
                    resourceId: node.resourceid
                }, function (response) {
                    if (common.dealResponse(response)){
                        $("#modal-apply-auth").modal('hide');
                        dialog.successTips('权限配置成功');
                    }
                });
            };
            //打开授权窗口
            this.openApplyAuthWin = function () {
                var node = that.treeTable.treegridData('getSelectedNode');
                if (!node || !node.resourceid) {
                    $("#modal-apply-auth").modal('hide');
                    dialog.errorTips('请选择权限数据行行进行操作');
                    return;
                }
                that.currNode = node;
                //加载岗位树
                role.loadRoleTree(that, function (response) {
                    $.fn.zTree.init($("#role-tree-list-auth"), {
                        view: {
                            selectedMulti: false
                        },
                        check: {
                            enable: true,
                            chkStyle: "checkbox",
                            //取消父子节点联动
                            chkboxType: {"Y": "", "N": ""}
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
                                if (treeNode.checked) {
                                    that.allocated(nums + 1);
                                } else {
                                    that.allocated(nums - 1);
                                }
                            },
                            //实现check
                            beforeCheck: function (treeId, treeNode) {
                                if (treeNode.id.indexOf('u') != -1)
                                    return false;
                            }
                        }
                    }, response.data);
                    //初始化权限分配的岗位信息
                    that.loadResourceRoles(node.resourceid);
                });
            };
            //删除资源
            this.deleteResource = function () {
                var node = that.treeTable.treegridData('getSelectedNode');
                if (!node || !node.resourceid) {
                    dialog.errorTips('请选择需要删除的数据行进行操作');
                    return;
                }
                if (!$('#treegrid-' + node.resourceid).treegrid('isLeaf')) {
                    dialog.errorTips('只能删除没有子权限的数据');
                    return;
                }

                dialog.confirm({msg: '确定删除该权限资源?', title: '删除权限'}).on(function (e) {
                    if (e) {
                        $.post('auth/delResource', {resourceId: node.resourceid}, function (response) {
                            if (common.dealResponse(response)) {
                                dialog.successTips('删除成功');
                                that.treeTable = that.treeTable.treegridData('reDraw');
                            }
                        });
                    }
                });

            };
            //编辑资源
            this.updateResource = function () {
                var node = that.treeTable.treegridData('getSelectedNode');
                var allData = that.treeTable.treegridData('getData');
                that.popTitle('编辑权限');
                ko.mapping.fromJS(node, that.authInfo);
                for (var i = 0; i < allData.length; i++) {
                    var obj = allData[i];
                    if (obj.resourceid == node.parentid)
                    //父权限
                        that.parentResName(obj.name);
                }
                that.authInfo.parentid(node.parentid);
                $("#modal-add-auth").modal('show');
            };
            //页面渲染完毕
            this.afterRender = function (element) {
                this.initEvent();
                this.initUI();
            };

            this.loadAuthTree = function () {
                $.get('json/queryResourceTree.json', function (response) {
                    if (common.dealResponse(response)) {
                        $.fn.zTree.init($("#auth-resource-tree-list"), {
                            view: {
                                selectedMulti: false
                            },
                            check: {
                                enable: true,
                                chkStyle: "checkbox",
                                //取消父子节点联动
                                chkboxType: {"Y": "", "N": ""}
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
                                //实现check
                                beforeCheck: function (event, treeId, treeNode) {
                                    var treeObj = common.tree.getTreeObj("auth-resource-tree-list");
                                    treeObj.checkAllNodes(false);
                                    return true;
                                },
                                onCheck: function (event, treeId, treeNode) {
                                    that.parentResName(treeNode.name);
                                    that.authInfo.parentid(treeNode.id);
                                }
                            }
                        }, response.data);
                    }
                });
            };
            this.initEvent = function () {
                $("#modal-add-auth").on('show.bs.modal', function () {
                    that.loadAuthTree();
                });
                $("#modal-apply-auth").on('shown.bs.modal', function () {
                    that.openApplyAuthWin();
                });
                $(document).on('click', '#updateResource', function () {
                    $(this).parent().parent().addClass('selected');
                    that.updateResource();
                });
            };
            this.loadAuthListTree = function (params) {
                //加载资源列表
                var tableid = 'auth-list-table';
                if(that.treeTable) {
                    that.treeTable = that.treeTable.treegridData('reDraw');
                    return;
                }

                that.treeTable = $('#' + tableid).treegridData({
                    tableid: tableid,
                    id: 'resourceid',
                    parentColumn: 'parentid',
                    url: 'json/queryResources.json',
                    ajaxParams: params, //请求数据的ajax的data属性
                    expandColumn: null,//在哪一列上面显示展开按钮
                    striped: true,   //是否各行渐变色
                    bordered: true,  //是否显示边框
                    success:function () {
                        //autoHeight();
                    },
                    expandAll: false,  //是否全部展开
                    columns: [
                        {
                            title: '权限名称',
                            field: 'name'
                        },
                        {
                            title: '导航地址',
                            field: 'hrefUrl'
                        },
                        {
                            title: '访问地址',
                            field: 'resurl'
                        },
                        {
                            title: '图标',
                            field: 'resIco'
                        },
                        {
                            title: '创建时间',
                            field: 'createTime'
                        },
                        {
                            title: '显示次序',
                            field: 'displayorder'
                        },
                        {
                            title: '资源类型',
                            field: function (item) {
                                var typeList = that.typeList();
                                for (var i = 0; i < typeList.length; i++) {
                                    var obj = typeList[i];
                                    if (obj.typeid == item.type) {
                                        if (item.type == 1)
                                            return "<span style='color: green;font-weight: bold'>" + obj.typename + "</span>";
                                        else if(item.type == 3)
                                            return "<span style='color: blue;font-weight: bold'>" + obj.typename + "</span>";
                                        else
                                            return "<span style='color: black;font-weight: bold'>" + obj.typename + "</span>";
                                    }
                                }
                            }
                        },
                        {
                            title: '操作',
                            defaultText: '<span id="updateResource" title="编辑" style="cursor: pointer"><i class="fa fa-edit" ></i></span>'
                        }
                    ]
                });
            };
            //构建系统界面
            this.initUI = function () {
                this.loadAuthListTree({});
                autoHeight();
            }

        }

        //岗位树高度自适应
        function autoHeight() {
            var windowHeight = $(window).height();
            var contentHeaderHeight = $(".content-tabs").height();
            var mainHeaderHeight = $(".main-header").height();
            var mainFooterHeight = $(".main-footer").height();
            var boxheader = $(".box-header").height();
            var boxHead = $("#boxHead").height();
            var thead = $("thead").height();
            var iheight = windowHeight - mainHeaderHeight - contentHeaderHeight - mainFooterHeight -boxHead -boxheader -thead-20;
            $("#authListBox").height(iheight);
            $("#authListBox").mCustomScrollbar({
                theme:"light-thin"
            });
        }

        $(window).resize(function () {
            autoHeight();
        });
        //export
        var auth = new auth();
        return auth;
    })
;
