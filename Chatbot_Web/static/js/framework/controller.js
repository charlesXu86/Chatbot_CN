define(['common', 'knockout-multimodels', 'tab', 'jquery', 'router', 'routes', 'index'], function (common, ko, tab, $) {
    function isEndSharp() { // url end with #
        if (controller.lastUrl != "" && location.toString().indexOf(controller.lastUrl) != -1 &&
            location.toLocaleString().indexOf('#') != -1 && location.hash == "") {
            return true;
        }
        return false;
    }
    var controller = {
        /**
         * 当前激活的页面和路由参数
         * @param pageName
         * @param routes
         */
        initJSAndCSS: function (pageName, route) {
            require([pageName + '-js', 'css!' + pageName + '-css'], function (page) {
                controller.init(pageName, page, route);
            });
        },
        init: function (pageName, pageData, route) {
            if (isEndSharp()) {
                return;
            }
            //使用TAB加载页面
            tab.addTabs({
                id: route.resurl,
                title: route.name,
                close: route.resurl == '/dashboard' ? false : true,
                url: paths[route.routeUrl + '-templates'],
                isIframe: route.isIframe,
                urlType: "relative",
                modelId: route.routeUrl,
                pageData: pageData,
                callback: function () {
                    pageData.init();
                    //每一个TAB页签绑定一个数据模型，以modelId进行区分
                    //绑定的数据模型对象也即每个define模块的返回值
                    //attach代替原有的applyBindings，因为后者只支持一个对象绑定
                    ko.attach(route.routeUrl, pageData);
                    pageData.afterRender();
                }
            });
        }
    };
    return controller;
});