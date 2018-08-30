define(['dialog', 'jquery'], function (dialog, $) {
    $.extend($.fn, {
        //将form表单参数转为Object
        serializeObject: function () {
            var o = {};
            var tempDisabled = $(this).find(":disabled");
            tempDisabled.removeAttr("disabled");
            var a = this.serializeArray();
            tempDisabled.attr("disabled", true);
            $.each(a, function () {
                if (o[this.name] !== undefined) {
                    if (!o[this.name].push) {
                        o[this.name] = [o[this.name]];
                    }
                    o[this.name].push(this.value || '');
                } else {
                    o[this.name] = this.value || '';
                }
            });
            return o;
        }
    });
    var common = {
        //jquery.datatable插件国际化
        lang: {
            "sProcessing": "处理中...",
            "sLengthMenu": "显示 _MENU_ 项结果",
            "sZeroRecords": "没有匹配结果",
            "sInfo": "显示第 _START_ 至 _END_ 项结果，共 _TOTAL_ 项",
            "sInfoEmpty": "显示第 0 至 0 项结果，共 0 项",
            "sInfoFiltered": "(由 _MAX_ 项结果过滤)",
            "sInfoPostFix": "",
            "sSearch": "搜索:",
            "sUrl": "",
            "sEmptyTable": "表中数据为空",
            "sLoadingRecords": "载入中...",
            "sInfoThousands": ",",
            "oPaginate": {
                "sFirst": "首页",
                "sPrevious": "上页",
                "sNext": "下页",
                "sLast": "末页"
            },
            "oAria": {
                "sSortAscending": ": 以升序排列此列",
                "sSortDescending": ": 以降序排列此列"
            }
        },
        domain: '',
        dic: {},
        getRootPath: function () {
            /*  var pathName = window.location.pathname.substring(1);
              var webName = pathName == '' ? '' : pathName.substring(0, pathName.indexOf('/'));
              if (webName == "") {
                  return window.location.protocol + '//' + window.location.host;
              }
              else {
                  return window.location.protocol + '//' + window.location.host + '/' + webName;
              }*/
            var baseUrl = window.document.location.protocol + "//" + window.document.location.host + "/";
            var shortenedUrl = window.document.location.href.replace(baseUrl, "");
            baseUrl = baseUrl + shortenedUrl.substring(0, shortenedUrl.indexOf("/"));
            return baseUrl;
        },
        //数组去重
        distinctArray: function (ary, key) {
            if (!ary || ary.length == 0)
                return [];
            var result = [], temp = {};
            for (var i = 0; i < ary.length; i++) {
                if (!temp[ary[i][key]]) {
                    result.push(ary[i]);
                    temp[ary[i][key]] = true;
                }
            }
            return result;
        },
        distinctSimpleArray: function (arr) {
            var obj = {},
                result = [],
                len = arr.length;
            for (var i = 0; i < arr.length; i++) {
                if (!obj[arr[i]]) { //如果能查找到，证明数组元素重复了
                    obj[arr[i]] = 1;
                    result.push(arr[i]);
                }
            }
            return result;
        }
        ,
        //ajax response
        dealResponse: function (response) {
            if (response.code == 0)
                return true;
            else if (response.code == 1)//超时
                document.location.href = this.getRootPath() + '/login';
            else
                dialog.tips({
                    message: response.message,
                    type: 'danger'
                });
            return false;
        },
        /**
         * 将列表转换为树的数组结构
         * @param nodesArray
         * @returns {*}
         */
        array2Nodes: function (nodesArray) {
            var i, l,
                key = "id",
                parentKey = "pId",
                childKey = "children";
            if (!key || key == "" || !nodesArray) return [];
            if (nodesArray instanceof Array) {
                var r = [];
                var tmpMap = {};
                for (i = 0, l = nodesArray.length; i < l; i++) {
                    tmpMap[nodesArray[i][key]] = nodesArray[i];
                }
                for (i = 0, l = nodesArray.length; i < l; i++) {
                    if (tmpMap[nodesArray[i][parentKey]] && nodesArray[i][key] != nodesArray[i][parentKey]) {
                        if (!tmpMap[nodesArray[i][parentKey]][childKey])
                            tmpMap[nodesArray[i][parentKey]][childKey] = [];
                        tmpMap[nodesArray[i][parentKey]][childKey].push(nodesArray[i]);
                    } else {
                        r.push(nodesArray[i]);
                    }
                }
                return r;
            } else {
                return [nodesArray];
            }
        },
        //ztree通用操作
        tree: {
            getTreeObj: function (treeid) {
                return $.fn.zTree.getZTreeObj(treeid);
            }
            ,

            getSelectedNode: function (treeid) {
                var treeObj = this.getTreeObj(treeid);
                var nodes = treeObj.getSelectedNodes();
                if (nodes)
                    return nodes[0];
            }
            ,

            updateNode: function (treeid, name, data) {
                var node = this.getSelectedNode(treeid);
                node.name = name;
                if (data)
                    node.data = data;
                this.getTreeObj(treeid).updateNode(node);
            },
            refreshNode: function (treeId) {
                var zTree = $.fn.zTree.getZTreeObj(treeId),
                    nodes = zTree.getSelectedNodes();
                for (var i = 0, l = nodes.length; i < l; i++) {
                    zTree.reAsyncChildNodes(nodes[i], 'refresh');
                }
            },
            /**
             * 模糊查找ztree
             * @param zTreeId
             * @param searchField
             * @param isHighLight
             * @param isExpand
             */
            fuzzySearch: function (zTreeId, searchField, isHighLight, isExpand) {
                var zTreeObj = $.fn.zTree.getZTreeObj(zTreeId);//get the ztree object by ztree id
                if (!zTreeObj) {
                    alter("fail to get ztree object");
                }
                var nameKey = zTreeObj.setting.data.key.name; //get the key of the node name
                isHighLight = isHighLight === false ? false : true;//default true, only use false to disable highlight
                isExpand = isExpand ? true : false; // not to expand in default
                zTreeObj.setting.view.nameIsHTML = isHighLight; //allow use html in node name for highlight use

                var metaChar = '[\\[\\]\\\\\^\\$\\.\\|\\?\\*\\+\\(\\)]'; //js meta characters
                var rexMeta = new RegExp(metaChar, 'gi');//regular expression to match meta characters

                // keywords filter function
                function ztreeFilter(zTreeObj, _keywords, callBackFunc) {
                    if (!_keywords) {
                        _keywords = ''; //default blank for _keywords
                    }

                    // function to find the matching node
                    function filterFunc(node) {
                        if (node && node.oldname && node.oldname.length > 0) {
                            node[nameKey] = node.oldname; //recover oldname of the node if exist
                        }
                        zTreeObj.updateNode(node); //update node to for modifications take effect
                        if (_keywords.length == 0) {
                            //return true to show all nodes if the keyword is blank
                            zTreeObj.showNode(node);
                            zTreeObj.expandNode(node, isExpand);
                            return true;
                        }
                        //transform node name and keywords to lowercase
                        if (node[nameKey] && node[nameKey].toLowerCase().indexOf(_keywords.toLowerCase()) != -1) {
                            if (isHighLight) { //highlight process
                                //a new variable 'newKeywords' created to store the keywords information
                                //keep the parameter '_keywords' as initial and it will be used in next node
                                //process the meta characters in _keywords thus the RegExp can be correctly used in str.replace
                                var newKeywords = _keywords.replace(rexMeta, function (matchStr) {
                                    //add escape character before meta characters
                                    return '\\' + matchStr;
                                });
                                node.oldname = node[nameKey]; //store the old name
                                var rexGlobal = new RegExp(newKeywords, 'gi');//'g' for global,'i' for ignore case
                                //use replace(RegExp,replacement) since replace(/substr/g,replacement) cannot be used here
                                node[nameKey] = node.oldname.replace(rexGlobal, function (originalText) {
                                    //highlight the matching words in node name
                                    var highLightText =
                                        '<span style="color: whitesmoke;background-color: darkred;">'
                                        + originalText
                                        + '</span>';
                                    return highLightText;
                                });
                                zTreeObj.updateNode(node); //update node for modifications take effect
                            }
                            zTreeObj.showNode(node);//show node with matching keywords
                            return true; //return true and show this node
                        }

                        zTreeObj.hideNode(node); // hide node that not matched
                        return false; //return false for node not matched
                    }

                    var nodesShow = zTreeObj.getNodesByFilter(filterFunc); //get all nodes that would be shown
                    processShowNodes(nodesShow, _keywords);//nodes should be reprocessed to show correctly
                }

                /**
                 * reprocess of nodes before showing
                 */
                function processShowNodes(nodesShow, _keywords) {
                    if (nodesShow && nodesShow.length > 0) {
                        //process the ancient nodes if _keywords is not blank
                        if (_keywords.length > 0) {
                            $.each(nodesShow, function (n, obj) {
                                var pathOfOne = obj.getPath();//get all the ancient nodes including current node
                                if (pathOfOne && pathOfOne.length > 0) {
                                    //i < pathOfOne.length-1 process every node in path except self
                                    for (var i = 0; i < pathOfOne.length - 1; i++) {
                                        zTreeObj.showNode(pathOfOne[i]); //show node
                                        zTreeObj.expandNode(pathOfOne[i], true); //expand node
                                    }
                                }
                            });
                        } else { //show all nodes when _keywords is blank and expand the root nodes
                            var rootNodes = zTreeObj.getNodesByParam('level', '0');//get all root nodes
                            $.each(rootNodes, function (n, obj) {
                                zTreeObj.expandNode(obj, true); //expand all root nodes
                            });
                        }
                    }
                }

                //listen to change in input element
                $(searchField).bind('input propertychange', function () {
                    var _keywords = $(this).val();
                    searchNodeLazy(_keywords); //call lazy load
                });

                var timeoutId = null;

                // excute lazy load once after input change, the last pending task will be cancled
                function searchNodeLazy(_keywords) {
                    if (timeoutId) {
                        //clear pending task
                        clearTimeout(timeoutId);
                    }
                    timeoutId = setTimeout(function () {
                        ztreeFilter(zTreeObj, _keywords); //lazy load ztreeFilter function
                        $(searchField).focus();//focus input field again after filtering
                    }, 500);
                }
            },
            /**
             * 递归获取每个节点下的所有子节点
             * @param ids
             * @param treeNode
             * @returns {*}
             */
            getChildren: function (ids, treeNode) {
                ids.push(treeNode.id);
                if (treeNode.isParent) {
                    for (var obj in treeNode.children) {
                        this.getChildren(ids, treeNode.children[obj]);
                    }
                }
                return ids;

            }
        },
        //设置图片显示区域为固定大小,方便后台按统一比例截取图片
        clacImgZoomParam: function (maxWidth, maxHeight, width, height) {
            var param = {top: 0, left: 0, width: width, height: height};
            if (width > maxWidth || height > maxHeight) {
                rateWidth = width / maxWidth;
                rateHeight = height / maxHeight;
                if (rateWidth > rateHeight) {
                    param.width = maxWidth;
                    param.height = Math.round(height / rateWidth);
                } else {
                    param.width = Math.round(width / rateHeight);
                    param.height = maxHeight;
                }
            }
            param.left = Math.round((maxWidth - param.width) / 2);
            param.top = Math.round((maxHeight - param.height) / 2);
            return param;
        }
    };

    //读取系统信息
    $.ajax({
        url: 'json/sysConfig.json',
        type: "GET",
        dataType: 'json',
        async: false,
        success: function (response) {
            if (common.dealResponse(response)) {
                common.domain = response.data.domain;
                common.dic = {
                    dutyData: response.data.dutyData,
                    tenantTypeData: response.data.tenantTypeData,
                    resourceTypeData: response.data.resourceTypeData,
                    bizKindData: response.data.bizKindData,
                    bizTypeData: response.data.bizTypeData,
                };
            }
        }
    });
    return common;
})
;