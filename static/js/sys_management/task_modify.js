var servers_selected = [];
var content_height = auto_height(91);
var select_server_grid = ""; //获取kendoUI grid对象
$('#date_start').kendoDatePicker({
    value: new Date(),
    format: "yyyy-MM-dd"
});

var task_id = $("#task_id").val()
var name = $("#task_name").val();
var ostype = $("#os_type").val();
var operationtype = $("#operation_type").val();
var timer_dataP = $("#date_start").data("kendoDatePicker");

var os_type = [{id: "W", text: 'Windows'}, {id: "L", text: 'Linux'}];
$("#sys_select .select2_box").select2({data: os_type});

if (os_type) {
    $("#sys_select .select2_box").select2("val", ostype);
}
selected = "01";
$("#date_start")[0].disabled = false;
$("#timer_minu")[0].disabled = false;
$("#timer_hour")[0].disabled = false;
timer_dataP.enable(true);

var operation_type = [{id: "R", text: '重启'}, {id: "S", text: '关机'}];
$("#operation_select .select2_box").select2({data: operation_type});
if (operationtype) {
    $("#operation_select .select2_box").select2("val", operationtype);
}

run_time = $("#task_run_time").val();
date_val = run_time.split(" ")[0];
time_val = run_time.split(" ")[1];
hour_val = time_val.split(":")[0];
minu_val = time_val.split(":")[1];
$("#timer_hour").val(hour_val);
$("#timer_minu").val(minu_val);
timer_dataP.value(date_val);


// $("#operation_select .select2_box").select2("val", "S");

// function change_value(selected) {
//     if (selected == "01") {
//         $("#date_start")[0].disabled = true;
//         $("#timer_minu")[0].disabled = true;
//         $("#timer_hour")[0].disabled = true;
//         timer_dataP.enable(false);
//     }
//     else if (selected == "02") {
//         $("#date_start")[0].disabled = false;
//         $("#timer_minu")[0].disabled = false;
//         $("#timer_hour")[0].disabled = false;
//         timer_dataP.enable(true);
//     }
// }
// change_value("02");

$(function () {
    $.post(site_url + "get_select_servers/", {
        task_id: $("#task_id").val()
    }, function (res) {
        server_list = res.data;
        servers_selected.splice(0, servers_selected.length);
        Array.prototype.push.apply(servers_selected, res.data);
        select_server_grid.dataSource.read();

    })
});


$("#check_add_page").css("height", content_height);

var grid_option = {
    pageable: false,
    dataSource: {
        data: servers_selected
    },
    columns: [
        {field: 'ip', title: 'IP地址'},
        {
            title: '操作', width: 60,
            template: '<div style="width:100%;text-align: center;"><a class="fa fa-trash-o" style="color:red;cursor: pointer" onclick="remove_server(\'\#= id \#\')"></a></div>'
        }
    ]
};

var select_server_grid = set_table("#server_list", grid_option);



function remove_server(id) {
    var server = {};
    for (var i = 0; i < servers_selected.length; i++) {
        if (servers_selected[i].id == id)
            server = servers_selected[i]
    }
    servers_selected.splice(servers_selected.indexOf(server), 1);
    select_server_grid.dataSource.read();
}

function add_server() {
    servers_selected.splice(0, servers_selected.length);
    var treeObj = $.fn.zTree.getZTreeObj("tree_sys");
    var select_servers = treeObj.getCheckedNodes(true);
    for (var i = 0; i < select_servers.length; i++) {
        if (select_servers[i].type == "IP") {
            servers_selected.push(select_servers[i]);
        }
    }
    select_server_grid.dataSource.read();
}

var tree_server = [];

var tree_option = {
    data: {
        key: {
            name: "name",
            checked: "checked"
        }
    },
    check: {enable: true},
    onClick: function (event, treeId, treeNode) {
        get_children(treeNode);
    },
    onCheck: function (event, treeId, treeNode) {
        get_all_children(treeNode);
    },
    enableAsyn: false
};

// var app_id_list = "";
// var app_id_list = "";
//
// function confirm() {
//     var os_type=$('input:radio[name="os_select"]:checked').val();
//     var operation_type=$('input:radio[name="operation_select"]:checked').val();
//     if (!os_type) {
//     app_alert("请确认系统类型！");
//     return;
//     }
//     if(servers_selected.length ==0){
//     app_alert("请选择服务器！");
//     return;
//     }
//     if (!operation_type) {
//     app_alert("请确认操作类型！");
//     return;
//     }
//     var data_info = {
//         servers: servers_selected,
//         os_type: os_type,
//         operation_type:operation_type
//     };
//     var data = JSON.stringify(data_info);
//     show_loading();
//     $.post(site_url + "fast_execute_script/", {"data": data}, function (res) {
//             close_loading();
//             if (res.is_success == "one") {
//                 app_alert("重启系统成功");
//             }
//             else if (res.is_success == "two") {
//                 app_alert(res.message);
//             }
//             else {
//                 app_alert(res.message);
//             }
//         }
//     ).error(function(error) {
//         close_loading();
//         if (error.status == 403) {
//             app_alert("没有权限")
//         }
//         else {
//             alert(error)
//         }
//
//     })
//
// }
function cancel() {
    window.location.reload()
}

function select_server() {
    var d = dialog({
        width: 350,
        title: '选择服务器',
        content: '<div style="width:100%;overflow-y: auto">\
    <div style="width:100%;overflow-y: auto">\
        <div style="width:100%;height:100%;">\
            <div style="width:100%;height:35px;">\
                <input type="text" class="form-control" id="sys_ip" style="width:70.5%;float: left;">\
                <button class="king-btn-demo king-btn king-primary" style="float:left;margin-left: 5px; " onclick="search_business();"><span style="line-height:0.2;" class="fa fa-search"></span>&nbsp;查找</button>\
            </div>\
            <div style="width: 100%; height: 100%;  padding-top: 5px;" id="sys_tree_div">\
                <div style="border:1px solid #ddd;overflow-y: auto;min-height: 300px" id="tree_sys" class="ztree"></div>\
            </div>\
        </div>\
    </div>\
</div>',
        onshow: function (arguments) {
            search_business();
        },
        okValue: '确定',
        ok: function () {
            show_loading();
            servers_selected.splice(0, servers_selected.length);
            app_id_list = "";
            var treeObj = $.fn.zTree.getZTreeObj("tree_sys");
            var select_servers = treeObj.getCheckedNodes(true);
            for (var i = 0; i < select_servers.length; i++) {
                if (select_servers[i].type == "IP") {
                    //servers_selected.push(select_servers[i]);
                    servers_selected.push({
                        ip: select_servers[i].ip,
                        app_id: select_servers[i].app_id,
                        source: select_servers[i].source,
                        id: select_servers[i].id
                    })
                }
                // if (select_servers[i].type == "first") {
                //     app_id_list += select_servers[i].id + ";";
                // }
            }
            $("#server_p").removeClass("display_none");
            select_server_grid.dataSource.read();
            close_loading();
        },
        cancelValue: '取消',
        cancel: function () {
            // do something
        }
    });
    d.showModal();
}

var tree_server = [];

var tree_option = {
    data: {
        key: {
            name: "name",
            checked: "checked"
        }
    },
    check: {enable: true},
    onClick: function (event, treeId, treeNode) {
        get_children(treeNode);
    },
    onCheck: function (event, treeId, treeNode) {
        get_all_children(treeNode);
    },
    enableAsyn: false
};

function search_business() {
    // var system_type = $("#sys_select .select2_box").select2("val");
    var sys_ip = $("#sys_ip").val();
    show_loading();
    if (sys_ip == "")
        get_business();
    else
        get_server_by_ip(sys_ip);
}

function get_server_by_ip(ip) {
    $.post(site_url + "get_sys_tree_by_ip/", {
        ip: ip
    }, function (res) {
        close_loading();
        if (!res.is_success) {
            app_alert(res.message);
            return;
        }
        tree_server = res.data;
        $("#sys_tree_div").children().remove();
        $("#sys_tree_div").append('<div style="border:1px solid #ddd;overflow-y: auto;min-height: 300px" id="tree_sys" class="ztree"></div>');
        set_ztree(tree_option, "#tree_sys", tree_server);
    })
}

function get_business() {
    $.post(site_url + "get_sys_tree/", {}, function (res) {
        close_loading();
        if (!res.result) {
            app_alert(res.message);
            return;
        }
        tree_server = res.data;
        $("#sys_tree_div").children().remove();
        $("#sys_tree_div").append('<div style="border:1px solid #ddd;overflow-y: auto;min-height: 300px" id="tree_sys" class="ztree"></div>');
        set_ztree(tree_option, "#tree_sys", tree_server);
    })
}

function get_all_children(treeNode) {
    if (treeNode.is_open) {
        if (treeNode.type == "first") {
            if (treeNode.children_add)
                return;
            else {
                $.post(site_url + "get_module_server/", {
                    "id": treeNode.id
                }, function (res) {
                    close_loading();
                    var treeObj = $.fn.zTree.getZTreeObj("tree_sys");
                    treeObj.removeChildNodes(treeNode);
                    for (var i = 0; i < res.data.length; i++) {
                        treeObj.addNodes(treeNode, res.data[i]);
                    }
                    treeNode.is_open = true;
                    treeNode.children_add = true;
                })
            }
        }
        else {
            return;
        }
    }
    show_loading();
    if (treeNode.type == "first") {
        $.post(site_url + "get_module_server/", {
            "id": treeNode.id
        }, function (res) {
            close_loading();
            var treeObj = $.fn.zTree.getZTreeObj("tree_sys");
            treeObj.removeChildNodes(treeNode);
            for (var i = 0; i < res.data.length; i++) {
                treeObj.addNodes(treeNode, res.data[i]);
            }
            treeNode.is_open = true;
            treeNode.children_add = true;
        })
    }
    else if (treeNode.type == "second") {
        var parent_id = treeNode.getParentNode().id;
        $.post(site_url + "get_server_by_module_id/", {"id": treeNode.id, "parent_id": parent_id}, function (res) {
            close_loading();
            var treeObj = $.fn.zTree.getZTreeObj("tree_sys");
            for (var i = 0; i < res.data.length; i++) {
                res.data[i].checked = true;
                res.data[i].icon = static_url + "img/server_icon.png";
                treeObj.addNodes(treeNode, res.data[i]);
            }
            treeNode.is_open = true;
        })
    }
    else {
        close_loading();
        return;
    }
}

function get_children(treeNode) {
    if (treeNode.is_open)
        return;
    show_loading();

    if (treeNode.type == "first") {
        $.post(site_url + "get_module_by_app_id/", {"id": treeNode.id}, function (res) {
            close_loading();
            var treeObj = $.fn.zTree.getZTreeObj("tree_sys");
            for (var i = 0; i < res.data.length; i++) {
                // res.data[i].checked = is_checked;
                treeObj.addNodes(treeNode, res.data[i]);
            }
            treeNode.is_open = true;
        })
    }
    else if (treeNode.type == "second") {
        var parent_id = treeNode.getParentNode().id;
        $.post(site_url + "get_server_by_module_id/", {"id": treeNode.id, "parent_id": parent_id}, function (res) {
            close_loading();
            var treeObj = $.fn.zTree.getZTreeObj("tree_sys");
            for (var i = 0; i < res.data.length; i++) {
                //res.data[i].checked = is_checked;
                res.data[i].icon = static_url + "img/server_icon.png";
                treeObj.addNodes(treeNode, res.data[i]);
            }
            treeNode.is_open = true;
        })
    }
    else {
        close_loading();
        return;
    }
}


function confirm() {
    var timeset = "";
    // var task_type = "I";
    timeset = $("#date_start").val();
    timeset = timeset + " " + $('#timer_hour').val() + ":" + $('#timer_minu').val() + ":00";
    if (!validate()) {
        app_alert('请检查必填项是否正确填写！');
        return;
    }
    var task_info = {
        task_id:task_id,
        name: $("#task_name").val(),
        os_type: $("#sys_select .select2_box").select2("val"),
        operation_type: $("#operation_select .select2_box").select2("val"),
        time_set: timeset,
        timer_hour: $("#timer_hour").val(),
        timer_minu: $("#timer_minu").val(),
        run_type: $("input[name='time_select']:checked").val(),
        servers: servers_selected,
    };
    var data = JSON.stringify(task_info);
    show_loading();
    $.post(site_url + "modify_task/", {"data": data}, function (res) {
            close_loading();
            if (res.is_success) {
                app_none_modal_alert("编辑修改成功！");
                search_task();
            } else {
                app_alert(res.message);
            }
        }
    )
}


var validate = function () {
    if ($("#task_name").val() == null || $("#task_name").val() == "")
        return false;
    if (servers_selected.length == 0)
        return false;
    if ($("#sys_select .select2_box").select2("val") == null || $("#sys_select .select2_box").select2("val") == "")
        return false;
    if ($("#operation_select .select2_box").select2("val") == null || $("#operation_select .select2_box").select2("val") == "")
        return false;
    if ($("input[name='time_select']:checked").val() == "TIMER" && (!$("#date_start").val()
        || !$("#timer_hour").val() || !$("#timer_minu").val()))
        return false;
    if ($("input[name='time_select']:checked").val() == "TIMER") {
        var date_sel = $("#date_start").val();
        date_sel = date_sel + " " + $('#timer_hour').val() + ":" + $('#timer_minu').val() + ":00";
        var errors = is_datetime(date_sel);
        if (errors != "") {
            return false;
        }
    }
    return true;
};