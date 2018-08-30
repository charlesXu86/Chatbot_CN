/**
 * 定义系统路由信息
 */
define(['jquery', 'common','index'], function ($, common,index) {
    var routes = {
        404: {
            title: '系统出错了'
        }
    };
    var sysNavMenusObj = index.sysNavMenus;
    function getResource(parentid) {
        for (var i = 0; i < sysNavMenusObj.length; i++) {
            var obj = sysNavMenusObj[i];
            if (obj.resourceid == parentid) {
                return obj;
            }
        }
    }
    if (sysNavMenusObj && sysNavMenusObj.length > 0) {
        for (var i = 0; i < sysNavMenusObj.length; i++) {
            var obj = sysNavMenusObj[i];
            if (obj.routeUrl && obj.type ==1) {
                routes[obj.routeUrl] = obj;
                if (obj.parentid)
                    obj.parent = getResource(obj.parentid).routeUrl;
            }
        }
    }
    routes.sysNavMenus = sysNavMenusObj;
    return routes;
});

sysNavMenus: [{
            "resourceid": 1,
            "name": "首页",
            "resIco": "fa fa-dashboard",
            "resurl": "/dashboard",
            "hrefUrl": "/",
            "type": 1,
            "displayorder": 100,
            "routeUrl": "dashboard",
            "childResourceList": []
        }, {
            "resourceid": 2,
            "name": "租户管理",
            "resIco": "fa fa-link",
            "resurl": "/tenant",
            "hrefUrl": "/tenant",
            "type": 1,
            "displayorder": 200,
            "routeUrl": "tenant",
            "childResourceList": []
        }
            , {
                "resourceid": 3,
                "name": "用户管理",
                "resIco": "fa fa-user-circle-o",
                "resurl": "/unit",
                "hrefUrl": "/user",
                "type": 1,
                "displayorder": 300,
                "routeUrl": "user",
                "childResourceList": [{
                    "resourceid": 4,
                    "name": "组织机构管理",
                    "resIco": "fa fa-university",
                    "resurl": "/unit",
                    "hrefUrl": "/user/unit",
                    "type": 1,
                    "parentid": 3,
                    "displayorder": 310,
                    "routeUrl": "unit",
                    "childResourceList": []
                }, {
                    "resourceid": 5,
                    "name": "岗位管理",
                    "resIco": "fa fa-id-card-o",
                    "resurl": "/role",
                    "hrefUrl": "/user/role",
                    "type": 1,
                    "parentid": 3,
                    "displayorder": 320,
                    "routeUrl": "role",
                    "childResourceList": []
                }, {
                    "resourceid": 6,
                    "name": "人员管理",
                    "resIco": "fa fa-user",
                    "resurl": "/human",
                    "hrefUrl": "/user/human",
                    "type": 1,
                    "parentid": 3,
                    "displayorder": 330,
                    "routeUrl": "human",
                    "childResourceList": []
                }, {
                    "resourceid": 7,
                    "name": "权限管理",
                    "resIco": "fa fa-lock",
                    "resurl": "/auth",
                    "hrefUrl": "/user/auth",
                    "type": 1,
                    "parentid": 3,
                    "displayorder": 340,
                    "routeUrl": "auth",
                    "childResourceList": []
                }]
            }, {
                "resourceid": 4,
                "name": "组织机构管理",
                "resIco": "fa fa-university",
                "resurl": "/unit",
                "hrefUrl": "/user/unit",
                "type": 1,
                "parentid": 3,
                "displayorder": 310,
                "routeUrl": "unit",
                "childResourceList": []
            }, {
                "resourceid": 5,
                "name": "岗位管理",
                "resIco": "fa fa-id-card-o",
                "resurl": "/role",
                "hrefUrl": "/user/role",
                "type": 1,
                "parentid": 3,
                "displayorder": 320,
                "routeUrl": "role",
                "childResourceList": []
            }, {
                "resourceid": 6,
                "name": "人员管理",
                "resIco": "fa fa-user",
                "resurl": "/human",
                "hrefUrl": "/user/human",
                "type": 1,
                "parentid": 3,
                "displayorder": 330,
                "routeUrl": "human",
                "childResourceList": []
            }, {
                "resourceid": 7,
                "name": "权限管理",
                "resIco": "fa fa-lock",
                "resurl": "/auth",
                "hrefUrl": "/user/auth",
                "type": 1,
                "parentid": 3,
                "displayorder": 340,
                "routeUrl": "auth",
                "childResourceList": []
            }, {
                "resourceid": 10,
                "name": "代码示例",
                "resIco": "fa fa-lock",
                "resurl": "/demo",
                "hrefUrl": "/demo",
                "type": 1,
                isIframe:true,
                "displayorder": 340,
                "routeUrl": "demo",
                "childResourceList": []
            }]