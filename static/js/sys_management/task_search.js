var num = 1;
var task_id = "";
var dataSource = [];
var height = auto_height(205);
$(function () {
    $("#table_task").css("height", height);
    search_task();

});
var grid_option = {
    height: height - 8,
    dataSource: {
        data: dataSource
    },
    columns: [
        {field: 'name', title: '任务名称'},
        {field: 'created_by', title: '创建者', width: 110},
        {field: 'when_created', title: '创建时间', width: 160},
        {field: 'run_type_value', title: '任务类型', width: 80},
        {field: 'time_set', title: '执行时间', width: 160},
        {
            title: '执行状态', width: 120,
            template: function (res) {
            var color_res = "";
            if (res.task_type == "DONE") {
                color_res = "fa fa-check color_green";
                res.status_name = "已完成";
            }
            else if (res.task_type == "WAITING") {
                color_res = "fa fa-bell";
                res.status_name = "待执行";
            }
            else if (res.task_type == "RUNNING"){
                color_res = "fa fa-spinner fa-pulse";
                res.status_name = "进行中";
            }
            else if (res.task_type == "FAIL"){
                color_res = "fa fa-info-circle color_red";
                res.status_name = "执行失败";
            }
            return "<span class='" + color_res + "'></span>&nbsp;" + res.status_name
            }
        },
        {
            title: '操作', width: 100,
            template: "<span title='编辑' style='cursor: pointer;color: blue' class='fa fa-pencil fa-lg onoperate' onclick='modify_task(\"\#= id \#\")'></span>&emsp;" +
            "<span title='删除' style='cursor: pointer;color: red;' class='fa fa-trash-o fa-lg onoperate' onclick='delete_task(\"\#= id \#\"" + ",this)'></span>"
        }
    ]
};

var task_grid = set_table("#task_list", grid_option);
var server_list = [];

function search_task() {
    var run_type = $("#time_type_select").val();
    show_loading();
    // if (run_type == "ALL")
    //     run_type = "";
    $.post(site_url + "search_check_task/", {
        // 'time_type': run_type,
        'name': $('#inp_task_name_filter').val()
    }, function (res) {
        for (var i = 0; i < res.data.length; i++) {
            if (res.data[i].run_type == "TIMER")
                res.data[i].run_type_value = "定时";
        }
        dataSource.splice(0, dataSource.length);
        Array.prototype.push.apply(dataSource, res.data);
        task_grid.dataSource.read();
        close_loading();
    }, 'json')
}

function modify_task(id) {
    show_loading();
    $.post(site_url + "get_task_modify_page/", {id: id}, function (res) {
        close_loading();
        var d = dialog({
            width: 850,
            title: '修改任务',
            content: res,
            okValue: '确定',
            ok: function () {
                return confirm();

            },
            cancelValue: '取消',
            cancel: function () {

            }
        });
        d.showModal();
    })
}
// var app_id_list = "";
// function confirm_form(id) {
//     var ipList = "";
//     var timeset = "";
//     var time_type = $("input[name='time_select']:checked").val();
//     var receivers = $("#receiver_mail .select2_box").select2("val");
//     if (!$("#task_name").val()) {
//         app_alert("任务名称不能为空！");
//         return false;
//     }
//     if (receivers.length == 0) {
//         app_alert("请选择接受报告邮箱！");
//         return false;
//     }
//     if (time_type != "NOW") {
//         if (time_type == "TIMER") {
//             timeset = $("#timer_date").val();
//             timeset = timeset + " " + ( $('#timer_hour').val() ? $('#timer_hour').val() : "00") + ":" + ($('#timer_minu').val() ? $('#timer_minu').val() : "00") + ":00"
//             var errors = is_datetime(timeset);
//             if (errors != "") {
//                 app_alert(errors);
//                 return false;
//             }
//         }
//         else {
//             if (!$("#day_long").val()) {
//                 app_alert("周期任务时间间隔不能为空！");
//                 return false;
//             }
//             if (!is_num($("#day_long").val())) {
//                 app_alert("周期任务时间间隔格式错误！");
//                 return false;
//             }
//             if ($("#day_long").val() == "0" || $("#day_long").val() == 0) {
//                 app_alert("时间间隔不能设置为0!");
//                 return false;
//             }
//             timeset = $("#per_date").val();
//             timeset = timeset + " " + ($('#per_hour').val() ? $('#per_hour').val() : "00") + ":" + ($('#per_minu').val() ? $('#per_minu').val() : "00") + ":00"
//             var errors = is_datetime(timeset);
//             if (errors != "") {
//                 app_alert(errors);
//                 return false;
//             }
//         }
//     }
//     var day_long = $("#day_long").val();
//     if (server_list.length == 0) {
//         app_alert("请选择服务器！");
//         return false;
//     }
//     for (var i = 0; i < server_list.length; i++) {
//         ipList += server_list[i].ip + ";"
//     }
//     var receiver = "";
//     for (var i = 0; i < receivers.length; i++) {
//         receiver += receivers[i] + ",";
//     }
//     receiver = receiver.substring(0, receiver.length - 1);
//     app_id_list = app_id_list.substring(0, app_id_list.length - 1);
//
//     var task_info = {
//         id: id,
//         name: $("#task_name").val(),
//         receivers: receiver,
//         time_type: time_type,
//         time_set: timeset,
//         servers: ipList,
//         day_long: day_long,
//         interval_type: $("#interval_type").val(),
//         app_id_list: app_id_list
//     };
//
//     var data = JSON.stringify(task_info);
//     show_loading();
//     $.post(site_url + "modify_check_task/", {"data": data}, function (res) {
//             close_loading();
//             if (res.is_success) {
//                 search_task();
//                 return;
//             }
//             else {
//                 app_alert(res.message);
//                 return false;
//             }
//         }
//     )
// }
//

// function start_task(id) {
//     show_loading();
//     $.post(site_url + "start_task/", {
//         "task_id": id
//     }, function (res) {
//         close_loading();
//         if (res.is_success) {
//             app_none_modal_alert("启动成功！");
//         } else {
//             app_alert(res.message);
//         }
//     })
// }

function delete_task(id, obj) {
    var d = dialog({
        width: 260,
        title: '删除任务',
        content: '确认要删除该任务吗？',
        okValue: '确定',
        ok: function () {
            show_loading();
            $.post(site_url + "delete_check_task/", {
                "id": id
            }, function (res) {
                close_loading();
                if (!res.is_success) {
                    alert(res.message);
                } else {
                    search_task();
                }
            })
        },
        cancelValue: '取消',
        cancel: function () {
            // do something
        }
    });
    d.show();
}
