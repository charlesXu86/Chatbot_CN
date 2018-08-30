define(['dialog','highcharts-exporting', 'common', 'knockout', 'knockout-mapping', 'jquery', 'gotoTop'], function (dialog,Highcharts, common, ko, mapping, $) {
    ko.mapping = mapping;
    var dashbord = {
        init: function () {
            var that = this;
            var currYear = new Date().getFullYear();
            this.queryYear = ko.observable(currYear);
            this.queryYear.subscribe(function (newValue) {
                that.requestAppStatisticsData('' + newValue);
            });
            this.tenantChart = null;
            dashbord.chart = null;
            var years = [];
            for (var i = 0; i < 10; i++) {
                var year = currYear - i;
                years.push({
                    yearName: year + "年",
                    year: year
                });
            }
            this.yearList = ko.observableArray(years);
            this.statisic = ko.mapping.fromJS({
                tenantCount: '',
                superTenantCount: '',
                adminTenantCount: '',
                normalTenantCount: '',
                humanCount: '',
                unitCount: '',
                roleCount: ''
            });
            this.appList = ko.observableArray();
            this.initStatisticsData();
        },
        //拉取统计数据
        initStatisticsData: function () {
            var that = this;
            $.get('json/userAndTenantStatistics.json', function (response) {
                if (common.dealResponse(response)) {
                    ko.mapping.fromJS(response.data, that.statisic);
                }
            });
        },
        afterRender: function (element) {
            this.initUI();
            this.queryAppByHumanId();
            this.initAppStatistics(this);
            this.initTenantStatistics(this);

        },
        initUI: function () {
            $('<a href="javascript:;" class="backToTop" title="返回顶部">返回顶部</a>').appendTo("body");
            $.fn.goToTop.def = {
                pageWidth: $(document).width(),//页面宽度
                pageWidthJg: 2,//按钮和页面的间隔距离
                pageHeightJg: 100,//按钮和页面底部的间隔距离
                startline: 200,//出现回到顶部按钮的滚动条scrollTop距离
                duration: 200,//回到顶部的速度时间
                targetObg: "body"//目标位置
            };
            $(".backToTop").goToTop();
            $(window).bind('scroll resize', function () {
                $(".backToTop").goToTop();
            });
        },
        //应用入口
        queryAppByHumanId: function () {
            var that = this;
            $.get('json/queryAppByHumanId.json', function (response) {
                if (common.dealResponse(response)) {
                    var appList = response.data;
                    if (appList && appList.length > 0) {
                        dashbord.appList.removeAll();
                        for (var i = 0; i < appList.length; i++) {
                            dashbord.appList.push(appList[i]);
                        }
                    }
                }
            });
        },
        //租户统计
        initTenantStatistics: function (self) {
            if (!document.getElementById('tenant-container'))
                return;
            dashbord.tenantChart = new Highcharts.Chart({
                chart: {
                    renderTo: 'tenant-container',
                    type: 'scatter',
                    zoomType: 'xy',
                    events: {
                        load: self.requestTenantStatisticsData // 图表加载完毕后执行的回调函数
                    }
                },
                title: {
                    text: '租户-人员-应用数据统计'
                },
                subtitle: {
                    text: '人员和应用关联情况'
                },
                xAxis: {
                    allowDecimals:false,
                    title: {
                        enabled: true,
                        text: '人员数'
                    },
                    startOnTick: true,
                    endOnTick: true,
                    showLastLabel: true
                },
                yAxis: {
                    allowDecimals:false,
                    title: {
                        text: '应用数'
                    }
                },
                plotOptions: {
                    scatter: {
                        marker: {
                            radius: 5,
                            states: {
                                hover: {
                                    enabled: true,
                                    lineColor: 'rgb(100,100,100)'
                                }
                            }
                        },
                        states: {
                            hover: {
                                marker: {
                                    enabled: false
                                }
                            }
                        },
                        tooltip: {
                            headerFormat: '',
                            pointFormat: '{point.name}:({point.x}, {point.y})'
                        }
                    }
                },
                series: [{
                    name: '租户',
                    color: 'rgba(223, 83, 83, .5)',
                    data: []
                }]
            });
        },
        requestTenantStatisticsData: function () {
            $.get('json/initTenantStatistics.json', function (response) {
                if (common.dealResponse(response)) {
                    var series = dashbord.tenantChart.series[0];
                    var users = response.data.users;
                    var apps = response.data.apps;
                    var data = [];
                    //租户可能只配置了应用或者人员
                    for (var i = 0; users && i < users.length; i++) {
                        var user = users[i];
                        var obj = {
                            name: user.NAME,
                            x: user.X
                        };

                        var hasApp = false;
                        for (var j = 0; apps && j < apps.length; j++) {
                            var app = apps[j];
                            if (app.NAME == user.NAME) {
                                obj.y = app.Y;
                                hasApp = true;
                            }
                        }
                        if (!hasApp)
                            obj.y = 0;
                        data.push(obj)
                    }
                    //反过来 配置了应用但是没配置人员
                    for (var i = 0; apps && i < apps.length; i++) {
                        var app2 = apps[i];
                        var obj2 = {
                            name: app2.NAME,
                            y: app2.Y
                        };

                        var hasUser = false;
                        for (var j = 0; users && j < users.length; j++) {
                            var user2 = users[j];
                            if (app2.NAME == user2.NAME) {
                                obj2.x = user2.X;
                                hasUser = true;
                            }
                        }
                        if (!hasUser)
                            obj2.x = 0;
                        var repeated = false;
                        for (var k = 0; k < data.length; k++) {
                            if (data[k].name == obj2.name) {
                                repeated = true;
                                break;
                            }
                        }
                        if (!repeated)
                            data.push(obj2);
                    }
                    series.setData(data);
                }
            });
        },
        //应用情况统计
        initAppStatistics: function (self) {
            if (!document.getElementById('app-container'))
                return;
            dashbord.chart = new Highcharts.Chart({
                chart: {
                    renderTo: 'app-container',
                    events: {
                        load: self.requestAppStatisticsData // 图表加载完毕后执行的回调函数
                    }
                },
                title: {
                    text: '应用发布和审批情况'
                },
                subtitle: {
                    text: '应用情况统计'
                },
                xAxis: {
                    allowDecimals:false,
                    title: {
                        text: '月份'
                    },
                    labels: {
                        formatter: function () {
                            return this.value + '月';
                        }
                    }
                },
                yAxis: {
                    allowDecimals:false,
                    title: {
                        text: '应用数量'
                    },
                    labels: {
                        formatter: function () {
                            return this.value + '个';
                        }
                    }
                },
                legend: {
                    layout: 'vertical',
                    align: 'right',
                    verticalAlign: 'middle'
                },
                plotOptions: {
                    series: {
                        label: {
                            connectorAllowed: false
                        },
                        pointStart: 1,
                        tooltip: {
                            headerFormat: ''
                        }
                    },
                    line: {
                        dataLabels: {
                            enabled: true
                        }
                    }
                },
                responsive: {
                    rules: [{
                        condition: {
                            maxWidth: 500
                        },
                        chartOptions: {
                            legend: {
                                layout: 'horizontal',
                                align: 'center',
                                verticalAlign: 'bottom'
                            }
                        }
                    }]
                },
                series: [{
                    name: '发布',
                    color: 'blue',
                    data: []
                }, {
                    name: '审批通过',
                    color: 'green',
                    data: []
                }, {
                    name: '审批拒绝',
                    color: 'red',
                    data: []
                }]
            });

        },
        requestAppStatisticsData: function () {
            $.get('json/initAppStatistics.json', {year: dashbord.queryYear()}, function (response) {
                if (common.dealResponse(response)) {
                    var series = dashbord.chart.series;
                    var published = response.data.published;
                    var accepted = response.data.accepted;
                    var refused = response.data.refused;
                    var empty = [null, null, null, null, null, null, null, null, null, null, null, null];
                    for (var i = 0; i < series.length; i++) {
                        var obj = series[i];
                        if (obj.name == '发布' && published) {
                            if (published.length == 0)
                                obj.setData(empty);
                            else
                                obj.setData(published);
                        }
                        if (obj.name == '审批通过' && accepted) {
                            if (accepted.length == 0)
                                obj.setData(empty);
                            else
                                obj.setData(accepted);
                        }
                        if (obj.name == '审批拒绝' && refused) {
                            if (refused.length == 0)
                                obj.setData(empty);
                            else
                                obj.setData(refused);
                        }
                    }
                }
            });
        }
    };

    return dashbord;
});