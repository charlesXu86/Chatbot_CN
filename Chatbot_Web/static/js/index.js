/**
 * 系统初始化入口
 * 系统布局，皮肤，滑动菜单
 */
define(['jquery.storageapi.min', 'jquery', 'controlSidebar', 'pushMenu', 'layout', 'bootstrap', 'tree'], function (Storages, $) {
    $('[data-toggle="control-sidebar"]').controlSidebar();
    $('[data-toggle="push-menu"]').pushMenu();

    var $pushMenu = $('[data-toggle="push-menu"]').data('lte.pushmenu');
    var $controlSidebar = $('[data-toggle="control-sidebar"]').data('lte.controlsidebar');
    var $layout = $('body').data('lte.layout');

    var subMenuClick = false;
    $(document).on('click', '#platformMenus .treeview', function (e) {
        $(this).siblings().removeClass('active');
        $(this).addClass('active');
    });

    /**
     * List of all the available skins
     *
     * @type Array
     */
    var mySkins = [
        'skin-blue',
        'skin-black',
        'skin-red',
        'skin-yellow',
        'skin-purple',
        'skin-green',
        'skin-blue-light',
        'skin-black-light',
        'skin-red-light',
        'skin-yellow-light',
        'skin-purple-light',
        'skin-green-light'
    ];
    //设置默认皮肤
    var storedSkin = get('skin');
    if (storedSkin) {
        $('body').addClass(storedSkin)
    } else {
        $('body').addClass('skin-blue')
    }

    /**
     * Get a prestored setting
     *
     * @param String name Name of of the setting
     * @returns String The value of the setting | null
     */
    function get(name) {
        if (typeof (Storage) !== 'undefined') {
            return localStorage.getItem(name);
        } else {//use plugins
            return Storages.localStorage.get(name);
        }
    }

    /**
     * Store a new settings in the browser
     *
     * @param String name Name of the setting
     * @param String val Value of the setting
     * @returns void
     */
    function store(name, val) {
        if (typeof (Storage) !== 'undefined') {
            localStorage.setItem(name, val)
        } else {//use plugins
            return Storages.localStorage.set(name, val);
        }
    }

    /**
     * Toggles layout classes
     *
     * @param String cls the layout class to toggle
     * @returns void
     */
    function changeLayout(cls) {
        $('body').toggleClass(cls);
        $layout.fixSidebar();
        if ($('body').hasClass('fixed') && cls == 'fixed') {
            $pushMenu.expandOnHover();
            $layout.activate()
        }
        $controlSidebar.fix()
    }

    /**
     * Replaces the old skin with the new skin
     * @param String cls the new skin class
     * @returns Boolean false to prevent link's default action
     */
    function changeSkin(cls) {
        $.each(mySkins, function (i) {
            $('body').removeClass(mySkins[i])
        });

        $('body').addClass(cls);
        store('skin', cls);
        return false
    }

    /**
     * Retrieve default settings and apply them to the template
     *
     * @returns void
     */
    function setup() {
        var tmp = get('skin');
        if (tmp && $.inArray(tmp, mySkins))
            changeSkin(tmp);

        // Add the change skin listener
        $('[data-skin]').on('click', function (e) {
            if ($(this).hasClass('knob'))
                return;
            e.preventDefault();
            changeSkin($(this).data('skin'))
        });

        // Add the layout manager
        $('[data-layout]').on('click', function () {
            changeLayout($(this).data('layout'))
        });

        $('[data-controlsidebar]').on('click', function () {
            changeLayout($(this).data('controlsidebar'));
            var slide = !$controlSidebar.options.slide;

            $controlSidebar.options.slide = slide;
            if (!slide)
                $('.control-sidebar').removeClass('control-sidebar-open')
        });
        $('.control-sidebar').mouseleave(function () {
            $(this).removeClass('control-sidebar-open')
        });

        $('[data-sidebarskin="toggle"]').on('click', function () {
            var $sidebar = $('.control-sidebar');
            if ($sidebar.hasClass('control-sidebar-dark')) {
                $sidebar.removeClass('control-sidebar-dark');
                $sidebar.addClass('control-sidebar-light')
            } else {
                $sidebar.removeClass('control-sidebar-light');
                $sidebar.addClass('control-sidebar-dark')
            }
        });

        $('[data-enable="expandOnHover"]').on('click', function () {
            $(this).attr('disabled', true);
            $pushMenu.expandOnHover();
            if (!$('body').hasClass('sidebar-collapse'))
                $('[data-layout="sidebar-collapse"]').click()
        });

        //  Reset options
        if ($('body').hasClass('fixed')) {
            $('[data-layout="fixed"]').attr('checked', 'checked')
        }
        if ($('body').hasClass('layout-boxed')) {
            $('[data-layout="layout-boxed"]').attr('checked', 'checked')
        }
        if ($('body').hasClass('sidebar-collapse')) {
            $('[data-layout="sidebar-collapse"]').attr('checked', 'checked')
        }

    }

    setup();

    $('[data-toggle="tooltip"]').tooltip();
    return {
        systemName: 'adminlte-plus',
        admin: 'adminlte-plus',
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
    };
});
