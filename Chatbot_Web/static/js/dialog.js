define(['jquery'], function ($) {
    var reg = new RegExp("\\[([^\\[\\]]*?)\\]", 'igm');
    var dialogHtml = "<div id=\"egova-dialog\" class=\"modal\">\n" +
        "    <div class=\"modal-dialog modal-sm\">\n" +
        "        <div class=\"modal-content\">\n" +
        "            <div class=\"modal-header\">\n" +
        "                <button type=\"button\" class=\"close\" data-dismiss=\"modal\"><span aria-hidden=\"true\">×</span><span class=\"sr-only\">Close</span></button>\n" +
        "                <h5 class=\"modal-title\"><i class=\"fa fa-exclamation-circle\"></i> [Title]</h5>\n" +
        "            </div>\n" +
        "            <div class=\"modal-body small\">\n" +
        "                <p>[Message]</p>\n" +
        "            </div>\n" +
        "            <div class=\"modal-footer\" >\n" +
        "                <button type=\"button\" class=\"btn btn-primary ok\" data-dismiss=\"modal\">[BtnOk]</button>\n" +
        "                <button type=\"button\" class=\"btn btn-default cancel\" data-dismiss=\"modal\">[BtnCancel]</button>\n" +
        "            </div>\n" +
        "        </div>\n" +
        "    </div>\n" +
        "</div>";
    var oldDialogHtml =  "    <div class=\"modal-dialog modal-sm\">\n" +
        "        <div class=\"modal-content\">\n" +
        "            <div class=\"modal-header\">\n" +
        "                <button type=\"button\" class=\"close\" data-dismiss=\"modal\"><span aria-hidden=\"true\">×</span><span class=\"sr-only\">Close</span></button>\n" +
        "                <h5 class=\"modal-title\"><i class=\"fa fa-exclamation-circle\"></i> [Title]</h5>\n" +
        "            </div>\n" +
        "            <div class=\"modal-body small\">\n" +
        "                <p>[Message]</p>\n" +
        "            </div>\n" +
        "            <div class=\"modal-footer\" >\n" +
        "                <button type=\"button\" class=\"btn btn-primary ok\" data-dismiss=\"modal\">[BtnOk]</button>\n" +
        "                <button type=\"button\" class=\"btn btn-default cancel\" data-dismiss=\"modal\">[BtnCancel]</button>\n" +
        "            </div>\n" +
        "        </div>\n" +
        "    </div>\n" ;
    var tipsHtml = "<div id='egova-tips' class=\"alert alert-dismissible\" style=\"text-align: center;display: none;position: absolute;top: 0;left: 50%;z-index: 99999;width: 250px\"></div>";
    $('body').append(dialogHtml).append(tipsHtml);
    var dialog = $("#egova-dialog");
    var $tips = $("#egova-tips");
    var _alert = function (options) {
        dialog.find('.ok').removeClass('btn-success').addClass('btn-primary');
        dialog.find('.cancel').hide();
        _dialog(options);

        return {
            on: function (callback) {
                if (callback && callback instanceof Function) {
                    dialog.find('.ok').click(function () {
                        callback(true)
                    });
                }
            }
        };
    };

    var _confirm = function (options) {
        dialog.find('.ok').removeClass('btn-primary').addClass('btn-success');
        dialog.find('.cancel').show();
        _dialog(options);

        return {
            on: function (callback) {
                if (callback && callback instanceof Function) {
                    dialog.find('.ok').click(function () {
                        callback(true)
                    });
                    dialog.find('.cancel').click(function () {
                        callback(false)
                    });
                }
            }
        };
    };

    var _dialog = function (options) {
        var ops = {
            msg: "",
            title: "操作提示",
            btnok: "确定",
            btncl: "取消"
        };

        $.extend(ops, options);

        var html = oldDialogHtml.replace(reg, function (node, key) {
            return {
                Title: ops.title,
                Message: ops.msg,
                BtnOk: ops.btnok,
                BtnCancel: ops.btncl
            }[key];
        });

        dialog.html(html);
        dialog.modal({
            width: 500,
            backdrop: 'static'
        });
    };

    var _tips = function (options) {
        var ops = {
            //warning ,info,success danger
            type: "info",
            message: '',
            speed: 2000
        };
        $.extend(ops, options);
        $tips.css({left: ($(window).width() - 250) / 2})
            .removeClass('alert-info').removeClass('alert-success').removeClass('alert-danger')
            .removeClass('alert-warning').addClass('alert-' + ops.type)
            .text(ops.message).fadeToggle(1000);
        setTimeout(function () {
            $tips.fadeToggle(1000);
        }, ops.speed);
    };
    //jquery global
    $.extend($.fn, {
        confirm: _confirm,
    });
    return {
        alert: function (msg) {
            _alert({msg:msg});
        },
        confirm: _confirm,
        tips: _tips,
        //便利方法
        errorTips: function (message) {
            _tips({
                message: message,
                type: 'danger'
            });
        }, infoTips: function (message) {
            _tips({
                message: message,
                type: 'info'
            });
        },
        successTips: function (message) {
            _tips({
                message: message,
                type: 'success'
            });
        },
        warningTips: function (message) {
            _tips({
                message: message,
                type: 'warning'
            });
        }
    }
});
