# -*- coding: utf-8 -*-
from common.mymako import render_mako_context, render_json
from common.log import logger
from home_application.models import *
import datetime
from blueking.component.shortcuts import get_client_by_request


def get_user_name(request):
    return request.user.username


def get_sys_tree(request):
    try:
        client = get_client_by_request(request)
        kwargs = {}
        result = client.cc.get_app_by_user(kwargs)
        if result["result"]:
            datas = result["data"]
            app_list = [{"name": data["ApplicationName"], "id": data["ApplicationID"],
                         "checked": False, "isParent": False, "type": "first",
                         "children_add": False, "is_open": False} for data in datas if data["ApplicationID"] != "1"]

        return render_json({"result": True, "data": app_list})
    except Exception, e:
        return render_json({"result": False, "error": e})


def get_module_by_appid(request):
    applicationID = request.POST.get("id")
    client = get_client_by_request(request)
    kwargs = {
        "app_id": applicationID
    }
    result = client.cc.get_app_host_list(kwargs)
    if result["result"]:
        return_data = []
        template_data = result["data"]
        module_ids = []
        for data in template_data:
            if data["ModuleID"] not in module_ids:
                module_ids.append(data["ModuleID"])
                return_data.append({"name": data["ModuleName"], "id": data["ModuleID"], "checked": False,
                                    "type": "second", "is_open": False, "isParent": False})
    else:
        return_data = []
    return render_json({"result": True, "data": return_data})


def get_module_server(request):
    applicationID = request.POST.get("id")
    client = get_client_by_request(request)
    kwargs = {
        "app_id": applicationID
    }
    result = client.cc.get_app_host_list(kwargs)
    if result["result"]:
        template_data = result["data"]
        module_ids = []
        return_data = []
        for data in template_data:
            if data["ModuleID"] not in module_ids:
                module_ids.append(data["ModuleID"])
                return_data.append({"name": data["ModuleName"], "id": data["ModuleID"], "checked": True,
                                    "type": "second", "is_open": True, "isParent": False})
        for module in return_data:
            datas = get_module_host_list(client, applicationID, module["id"])
            module["children"] = [
                {"name": "[" + data["InnerIP"] + "] " + data["HostName"],
                 "id": str(data["InnerIP"]).replace('.', '_'), "ip": data["InnerIP"], "type": "IP", "checked": True,
                 "icon": "../../static/images/server_icon.png", "source": data["Source"],
                 "app_id": data["ApplicationID"]}
                for data in datas]
    else:
        return_data = []
    return render_json({"result": True, "data": return_data})


def get_server_by_module_id(request):
    client = get_client_by_request(request)
    app_id = request.POST.get("parent_id")
    module_id = request.POST.get("id")
    kwargs = {
        "app_id": app_id,
        "module_id": module_id
    }
    result = client.cc.get_module_host_list(kwargs)
    if result["result"]:
        datas = result["data"]
    else:
        datas = []
    return_data = [
        {"name": "[" + data["InnerIP"] + "] " + data["HostName"], "is_open": True, "isParent": False,
         "id": str(data["InnerIP"]).replace('.', '_'), "checked": False, "ip": data["InnerIP"], "type": "IP",
         "icon": "../../static/images/server_icon.png", "source": data["Source"], "app_id": data["ApplicationID"]}
        for data in datas]
    return render_json({"result": True, "data": return_data})


def get_module_by_app_id(client, applicationID):
    kwargs = {
        "app_id": applicationID
    }
    result = client.cc.get_app_host_list(kwargs)
    if result["result"]:
        return_data = []
        template_data = result["data"]
        module_ids = []
        for data in template_data:
            try:
                if data["ModuleID"] not in module_ids:
                    module_ids.append(data["ModuleID"])
                    return_data.append({"name": data["ModuleName"], "id": data["ModuleID"], "checked": False,
                                        "type": "second", "is_open": False, "isParent": False, "children": []})
            except Exception, e:
                logger.error(e.message)
        return return_data
    else:
        return []


def get_module_host_list(client, app_id, module_id):
    kwargs = {
        "app_id": app_id,
        "module_id": module_id
    }
    result = client.cc.get_module_host_list(kwargs)
    if result["result"]:
        return result["data"]
    else:
        return []

def get_sys_tree_by_id(request):
    task_id = request.POST.get("task_id")
    check_task = Task.objects.get(id=task_id)
    servers = check_task.task_server_set.all().values('ip')
    server_select = [server["ip"] for server in servers]
    try:
        client = get_client_by_request(request)
        kwargs = {}
        result = client.cc.get_app_by_user(kwargs)
        if result["result"]:
            datas = result["data"]
            app_list = [{"name": data["ApplicationName"], "id": data["ApplicationID"],
                         "checked": False, "isParent": True, "type": "first",
                         "children": [], "children_add": True,
                         "is_open": False} for data in datas if data["ApplicationID"] != "1"]
        for app in app_list:
            # if app["Default"] == "0":
            app["children"] = get_module_by_app_id(client, app["id"])
            for module in app["children"]:
                # if module["Default"] == "0" and module["name"] != "中间件模块":
                datas = get_module_host_list(client, app["id"], module["id"])
                for data in datas:
                    temp_server = {
                        "name": "[" + data["InnerIP"] + "] " + data["HostName"],
                        "id": str(data["InnerIP"]).replace('.', '_'), "icon": "../../static/images/server_icon.png",
                        "ip": data["InnerIP"], "type": "IP" ,"source":data["Source"],"app_id":data["ApplicationID"]
                    }
                    if temp_server["ip"] in server_select:
                        temp_server["checked"] = True
                    module["children"].append(temp_server)
                    # module["modules"] = [
                    #     {"name": "[" + data["InnerIP"] + "] " + data["HostName"],
                    #      "id": str(data["InnerIP"]).replace('.', '_'), "ip": data["InnerIP"], "type": "IP"}
                    #     for data in datas]

        return render_json({"result": True, "data": app_list})
    except Exception, e:
        return render_json({"result": False, "error": e})


def insert_log(operator, ostype, operationtype, tasktype, operated_detail):
    date_now = str(datetime.datetime.now()).split(".")[0]
    Operation_log.objects.create(operator=operator, ostype=ostype, operationtype=operationtype, tasktype=tasktype, operated_detail=operated_detail,
                                 when_created=date_now)


def get_select_servers(request):
    try:
        task_id = request.POST.get("task_id")
        servers = Task.objects.get(id=task_id).servers
        data = eval(servers)
        return render_json({"data": data})
    except Exception, e:
        logger.error(e.message)
        return render_json({"is_success": False, "message": e.message})