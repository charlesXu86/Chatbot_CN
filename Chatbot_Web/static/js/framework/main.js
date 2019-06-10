/**
 * 异步加载模块入口，每个js库的css也作为依赖进行按需加载
 * @type {{jquery: string, routes: string, knockout: string, router: string, moment: string, controller: string, appRouter: string, "knockout-mapping": string, "knockout-amd-helpers": string, "knockout-multimodels": string, text: string, bootstrap: string, icheck: string, "icheck-css": string, "jquery.livequery": string, "datatables.net": string, "dataTables.select-css": string, "dataTables.select": string, "datatables.net-bs": string, "datatables.net-bs-css": string, "responsive.bootstrap": string, "responsive.bootstrap-css": string, "dataTables.responsive": string, select2: string, "select2-css": string, "ztree-css": string, "jquery.ztree.core": string, "jquery.ztree.excheck": string, "jquery.ztree.exedit": string, "jquery.ztree.exhide": string, gotoTop: string, pushMenu: string, controlSidebar: string, layout: string, tree: string, "jquery.slimscroll": string, "jquery.storageapi.min": string, app: string, common: string, dialog: string, "404-templates": string, "404-js": string, "404-css": string, "dashboard-templates": string, "dashboard-js": string, "dashboard-css": string, "tenant-templates": string, "tenant-js": string, "tenant-css": string, "unit-templates": string, "unit-js": string, "unit-css": string, "role-templates": string, "role-js": string, "role-css": string, "human-templates": string, "human-js": string, "human-css": string}}
 */
var paths = {
    //framework
    'jquery': 'js/lib/jquery.min',
    'routes': 'js/framework/routes',
    'knockout': 'js/lib/knockout/knockout',
    'router': 'js/lib/knockout/director',
    'moment': 'js/lib/moment/moment.min',
    'controller': 'js/framework/controller',
    'appRouter': 'js/framework/router',
    "knockout-mapping": "js/lib/knockout/knockout-mapping",
    "knockout-multimodels": "js/lib/knockout/knockout-multimodels.min",
    "text": "js/lib/require/text",
    'bootstrap': 'js/lib/bootstrap.min',
    'icheck': 'js/lib/jquery.plugin/icheck.min',
    'icheck-css': 'css/lib/icheck-blue',
    'jquery.livequery': 'js/lib/jquery.plugin/jquery.livequery',
    'jquery.blockui': 'js/lib/jquery.blockui',
    //dataTable
    'datatables.net': 'js/lib/datatable/jquery.dataTables.min',
    'dataTables.select-css': 'css/lib/select.bootstrap.min',
    'dataTables.select': 'js/lib/datatable/dataTables.select.min',
    'datatables.net-bs': 'js/lib/datatable/dataTables.bootstrap.min',
    'datatables.net-bs-css': 'css/lib/dataTables.bootstrap.min',
    'responsive.bootstrap': 'js/lib/datatable/responsive.bootstrap.min',
    'responsive.bootstrap-css': 'css/lib/responsive.bootstrap.min',
    'dataTables.responsive': 'js/lib/datatable/dataTables.responsive.min',
    //highcharts
    'highcharts': "js/lib/highcharts/highcharts",
    //ie9以下hacker
    'highcharts-oldie': "js/lib/highcharts/oldie",
    'highcharts-map': "js/lib/highcharts/modules/map",
    'highcharts-drilldown': "/js/lib/highcharts/modules/drilldown",
    'highcharts-exporting': "js/lib/highcharts/modules/exporting",
    //treegrid
    'jquery.treegrid-css': 'css/lib/jquery.treegrid',
    'jquery.treegrid': 'js/lib/treegrid/jquery.treegrid.min',
    'jquery.treegrid.extension': 'js/lib/treegrid/jquery.treegrid.extension',
    //select2
    'select2': 'js/lib/select2/select2.full.min',
    'select2-css': 'css/lib/select2.min',
    //ztree
    "ztree-css": "css/lib/ztree",
    "jquery.ztree.core": "js/lib/ztree/jquery.ztree.core.min",
    "jquery.ztree.excheck": "js/lib/ztree/jquery.ztree.excheck.min",
    "jquery.ztree.exedit": "js/lib/ztree/jquery.ztree.exedit.min",
    "jquery.ztree.exhide": "js/lib/ztree/jquery.ztree.exhide.min",
    //bootstrap step
    'wizard': 'js/lib/wizard/jquery.bootstrap.wizard.min',
    //gotoTop
    "gotoTop": "js/lib/jquery.plugin/goto.top",
    //lib
    'pushMenu': 'js/lib/adminlte/pushMenu',
    'controlSidebar': 'js/lib/adminlte/controlSidebar',
    'layout': 'js/lib/adminlte/layout',
    'tree': 'js/lib/adminlte/tree',
    'tab': 'js/lib/adminlte/tab',
    'mCustomScrollbar': 'js/lib/jquery.mCustomScrollbar.concat.min',
    'jquery.slimscroll': 'js/lib/jquery.plugin/jquery.slimscroll.min',
    'jquery.storageapi.min': 'js/lib/jquery.plugin/jquery.storageapi.min',
    'jquery-ui-widget': 'js/lib/jquery-file-upload/jquery.ui.widget',
    'jquery.fileupload': 'js/lib/jquery-file-upload/jquery.fileupload',
    'jquery.iframe-transport': 'js/lib/jquery-file-upload/jquery.iframe-transport',
    'jquery.imgareaselect': 'js/lib/jquery.imgareaselect.min',
    //业务，html获取通过对应的controller获取，整个生命周期页面只会加载一次
    'index': 'js/index',
    'common': 'js/common',
    //弹框组件
    'dialog': 'js/dialog',
    //404
    '404-html': 'templates/404/404.html',
    '404-js': 'templates/404/404',
    '404-css': 'templates/404/404',
    //首页
    'dashboard-html': 'templates/dashboard/dashboard.html',
    'dashboard-js': 'templates/dashboard/dashboard',
    'dashboard-css': 'templates/dashboard/dashboard',
    //中文分词
    'cws-html': 'templates/cws/cws.html',
    'cws-js': 'templates/cws/cws',
    'cws-css': 'templates/cws/cws',
    //词性标注
    'unit-html': 'templates/user/unit.html',
    'unit-js': 'templates/user/unit/unit',
    'unit-css': 'templates/user/unit/unit',
    //信息抽取
    'role-html': 'templates/user/role.html',
    'role-js': 'templates/user/role/role',
    'role-css': 'templates/user/role/role',
    //自然语言理解
    'human-html': 'templates/user/human.html',
    'human-js': 'templates/user/human/human',
    'human-css': 'templates/user/human/human',
    //句法分析
    'auth-html': 'templates/user/auth.html',
    'auth-js': 'templates/user/auth/auth',
    'auth-css': 'templates/user/auth/auth',
    //语义分析
    'demo-html': 'templates/demo/demo.html',
    'demo-js': 'templates/demo/demo',
    'demo-css': 'templates/demo/demo',
    //自然语言生成
    'demo-html': 'templates/demo/demo.html',
    'demo-js': 'templates/demo/demo',
    'demo-css': 'templates/demo/demo',
    //多伦对话
    'demo-html': 'templates/demo/demo.html',
    'demo-js': 'templates/demo/demo',
    'demo-css': 'templates/demo/demo',
    //强化学习
    'demo-html': 'templates/demo/demo.html',
    'demo-js': 'templates/demo/demo',
    'demo-css': 'templates/demo/demo',
    //知识图谱
    'demo-html': 'templates/demo/demo.html',
    'demo-js': 'templates/demo/demo',
    'demo-css': 'templates/demo/demo',
    //核心架构
    'demo-html': 'templates/demo/demo.html',
    'demo-js': 'templates/demo/demo',
    'demo-css': 'templates/demo/demo',
    //人机对话
    'demo-html': 'templates/demo/demo.html',
    'demo-js': 'templates/demo/demo',
    'demo-css': 'templates/demo/demo',
    //用户管理
    'demo-html': 'templates/demo/demo.html',
    'demo-js': 'templates/demo/demo',
    'demo-css': 'templates/demo/demo',
};

var baseUrl = '/adminlte-plus/';

require.parameters({
    baseUrl: baseUrl,
    paths: paths,
    //css插件配置
    map: {
        '*': {
            'css': 'js/lib/require/css'
        }
    },
    //非AMD模块
    shim: {
        'router': {
            exports: 'Router'
        },
        //jquery库都导出为jquery
        'bootstrap': ['jquery'],
        'pushMenu': ['jquery'],
        'gotoTop': ['jquery'],
        'jquery.imgareaselect': ['jquery'],
        'icheck': ['jquery', 'css!icheck-css'],
        'tree': ['jquery'],
        'controlSidebar': ['jquery'],
        'jquery.blockui': ['jquery'],
        'wizard': ['jquery'],
        'layout': ['jquery', 'jquery.slimscroll'],
        'jquery.livequery': ['jquery'],
        'mCustomScrollbar': ['jquery'],
        'jquery.slimscroll': ['jquery'],
        'jquery.ztree.core': ['jquery', 'css!ztree-css'],
        'jquery.ztree.excheck': ['jquery', 'jquery.ztree.core'],
        'jquery.ztree.exhide': ['jquery', 'jquery.ztree.core'],
        'jquery.ztree.exedit': ['jquery', 'jquery.ztree.core'],
        'jquery.storageapi.min': {
            'exports': 'Storages'
        },
        'jquery.treegrid': ['jquery', 'css!jquery.treegrid-css'],
        'jquery.treegrid.extension': ['jquery.treegrid'],
        //highcharts通过require需要pacth -> https://stackoverflow.com/questions/8186027/loading-highcharts-with-require-js
        'highcharts': {
            'exports': "Highcharts"
        },
        'highcharts-oldie': {
            'exports': "Highcharts",
            'deps': ["highcharts"]
        },
        'highcharts-map': {
            'exports': "Highcharts",
            'deps': ["highcharts"]
        },
        'highcharts-drilldown': {
            'exports': "Highcharts",
            'deps': ["highcharts"]
        },
        'highcharts-exporting': {
            'exports': "Highcharts",
            'deps': ["highcharts"]
        }
    }
});

require(['jquery', "knockout-multimodels", 'appRouter', 'index', 'routes'], function ($, ko, router, index) {
    function autoHeight() {
        var windowHeight = $(window).height();
        var mainHeaderHeight = $(".main-header").height();
        var mainFooterHeight = $(".main-footer").height();
        var iheight = windowHeight - mainHeaderHeight - mainFooterHeight;
        $("#iframeDiv").height(iheight);
    }

    var showPlatform = {
        isShowPlatform: ko.observable(true)
    };
    index.showPlatfrom = function () {
        showPlatform.isShowPlatform(true);
        $(".content-tabs").show();
        $(".content-pages").show();
        $("#iframeDiv").hide();
    };
    index.showApp = function () {
        showPlatform.isShowPlatform(false);
        $(".content-tabs").hide();
        $(".content-pages").hide();
        $("#iframeDiv").show();
    };
    autoHeight();
    $(window).resize(function () {
        autoHeight();
    });
    showPlatform.sysNavMenus = index.sysNavMenus;
    ko.attach('mainHeader', index);
    ko.attach('mainSidebar', showPlatform);
    index.showPlatfrom();
});

