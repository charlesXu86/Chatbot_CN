define(['knockout', 'controller', 'routes', 'router', 'jquery'], function (ko, controller, routes, Router, $) {
    function dispatch(path) {
        var route = routes[path];
        if (!route.hrefUrl) return;
        if (route.hrefUrl.indexOf('#') == -1)
            route.hrefUrl = '#' + route.hrefUrl;
        controller.initJSAndCSS(path, route);
    }

    //初始化路由
    var router = new Router().configure({
        //404
        notfound: function () {
            dispatch('404');
        },
        html5history: false
    });
    //根据系统菜单设置路由
    var sysNavMenus = routes.sysNavMenus;
    if (sysNavMenus && sysNavMenus.length > 0) {
        for (var i = 0; i < sysNavMenus.length; i++) {
            var obj = sysNavMenus[i];
            //非导航类数据
            if (obj.type != 1)
                continue;
            //立即执行路由绑定
            (function (obj) {
                router.on(obj.hrefUrl, function () {
                    var url = obj.routeUrl;
                    //直接打开子菜单链接
                    if (obj.parentid)
                        dispatch(url);
                    else {//当前是父菜单
                        var childResourceList = obj.childResourceList;
                        //有二级菜单
                        if (childResourceList && childResourceList.length > 0)
                            dispatch(childResourceList[0].routeUrl);
                        else//只有一个根菜单
                            dispatch(url);
                    }
                });
            })(obj);
        }
    }
    var urlNotAtRoot = window.location.pathname && (window.location.pathname != baseUrl);

    if (urlNotAtRoot) {
        router.init();
    } else {
        router.init('/');
    }
    document.location.href = "#" + sysNavMenus[0].hrefUrl;
    return router;
});