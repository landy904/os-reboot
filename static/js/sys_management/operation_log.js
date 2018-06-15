/**
 * Created by kido on 2016/10/14.
 */

var dateStart = new Date();
$('#time_start_s').kendoDatePicker({
    value: new Date(dateStart.setDate(dateStart.getDate() - 30)),
    format: "yyyy-MM-dd"
});

$('#time_end_s').kendoDatePicker({
    value: new Date(),
    format: "yyyy-MM-dd"
});


var height = auto_height(230);
var dataSource = [
//    {account_name:"iven",mail_address:"iven@canway.net",id:1234}
];
$(function () {
    $("#log_list").css("height", height);
    get_log_list();
});
var grid_option={
    dataSource: {
        data: dataSource
    },
    height:height,
    columns:[
        {field: 'operator', title: '操作者' ,width:120},
        {field: 'when_created', title: '操作时间' ,width:180},
        {field: 'ostype', title: '系统类型' ,width:80},
        {field: 'operationtype', title: '操作类型' ,width:80},
        {field: 'tasktype', title: '执行类型' ,width:80},
        {field: 'operated_detail', title: '日志信息'}
    ]
};
var log_grid = set_table("#log_list", grid_option);


function get_log_list() {
    show_loading();
    var log_operator = $("#operator_s").val();
    var time_start = $("#time_start_s").val();
    var time_end_temp = $("#time_end_s").val();
    var time_end = new Date(new Date().setDate(new Date(time_end_temp).getDate() + 1));
    var time_end_value= time_end.Format("yyyy-MM-dd");
    $.post(site_url+"get_log_list/", {
         "log_operator": log_operator,
         "time_start": time_start,
         "time_end": time_end_value
    }, function (res) {
        close_loading();
        if (res.is_success) {
            dataSource.splice(0, dataSource.length);
            Array.prototype.push.apply(dataSource, res.data);
            log_grid .dataSource.read();
        }
        else {
            app_alert(res.message);
        }
    })
}

