# -*- coding: utf-8 -*-
from celery import task
from celery.schedules import crontab
from celery.task import periodic_task
from common.log import logger
from blueking.component.shortcuts import get_client_by_user
from conf.default import APP_ID, APP_TOKEN, BK_PAAS_HOST
import base64
import time
import datetime
from home_application.models import *
from home_application.enums import *
import json
from home_application.enums import *
from home_application.helper import *



# """
# celery 任务示例
#
# 本地启动celery命令: python  manage.py  celery  worker  --settings=settings
# 周期性任务还需要启动celery调度命令：python  manage.py  celerybeat --settings=settings
# """



@task()
def run_check_task(user_name, task_id,celery_set_id):
    logger.info(u"开始执行")
    check_task = Task.objects.get(id=task_id)
    if check_task.run_type == "NOW":
        tasktype = u"立即"
    elif check_task.run_type == "TIMER":
        tasktype = u"定时"
    if check_task.os_type == "L":
        ostype = u"Linux"
    elif check_task.os_type == "W":
        ostype = u"Windows"
    if check_task.operation_type == "R":
        operationtype = u"重启"
    elif check_task.operation_type == "S":
        operationtype = u"关机"
    celery_set = celery_task_control.objects.get(id=celery_set_id)
    check_task.task_type = TASK_STATUS_TYPE.RUNNING
    check_task.save()
    if celery_set.is_stop and celery_set.run_type != RUN_TYPE.NOW:
        return
    logger.info(u"开始执行任务%s" % check_task.name)
    try:
        client = get_client_by_user(user_name)
        date_now = str(datetime.datetime.now()).split(".")[0]
        check_apps = set_check_apps(check_task.servers)
        param = None
        for check_app in check_apps:
            info_result = run_check_server(check_app, client, user_name, param, task_id)
            logger.info(u"执行成功")
        celery_set.is_stop = True
        celery_set.save()
        ips_fail = ''
        ips_sucess = ''
        for i in info_result:
            if i["result"] == True:
                ips_sucess = i["ips"]
            elif i["result"] == False:
                ips_fail = i["ips"]
        if len(ips_fail) == 0:
            logger.info(u"执行成功")
            operated_detail = u"执行任务 : " + check_task.name + u"  全部服务器执行成功：" + ",".join(ips_sucess)
            check_task.task_type = TASK_STATUS_TYPE.DONE
            check_task.save()
        elif len(ips_sucess) == 0:
            operated_detail = u"执行任务 : " + check_task.name + u";全部服务器执行失败：" + ",".join(ips_fail)
            logger.info(u"执行失败")
            check_task.task_type = TASK_STATUS_TYPE.FAIL
            check_task.save()
        else:
            operated_detail = u"执行任务 : " + check_task.name + u"  执行成功服务器：" + ",".join(ips_sucess) + u"; 执行失败服务器" + ",".join(ips_fail)
            logger.info(u"执行失败")
            check_task.task_type = TASK_STATUS_TYPE.FAIL
            check_task.save()
        insert_log(user_name, ostype, operationtype, tasktype, operated_detail)
        return ips_sucess,ips_fail
    except Exception, e:
        check_task.task_type = TASK_STATUS_TYPE.FAIL
        check_task.save()
        operated_detail = u"执行任务失败 : " + check_task.name
        insert_log(user_name, ostype, operationtype, tasktype, operated_detail)
        logger.error(u"任务“%s”执行失败" % check_task.name)
        logger.error(e.message)



def run_check_server(check_app, client, user_name, param, task_id):
    info_result = fast_execute_script(check_app, client, user_name, param_content=param,
                                      script_timeout=120, task_id=task_id)
    if info_result:
        return info_result


def fast_execute_script(check_app, client, user_name, param_content=None, script_timeout=1000, task_id=None):
    import sys
    reload(sys)
    task_info = Task.objects.get(id=task_id)
    os_type = task_info.os_type
    operation_type = task_info.operation_type
    if os_type == "L":
        if operation_type == "S":
            script_content = "shutdown -h now"
        elif operation_type == "R":
            script_content = "shutdown -r now"
        type = "1"
        account = "root"
    elif os_type == "W":
        if operation_type == "S":
            script_content = "shutdown -s -t 0"
        elif operation_type == "R":
            script_content = "shutdown -r  -t 0"
        type = "2"
        account = "administrator"
    sys.setdefaultencoding('utf-8')
    kwargs = {
        "app_code": APP_ID,
        "app_secret": APP_TOKEN,
        "app_id": check_app["app_id"],
        "username": user_name,
        "content": base64.encodestring(script_content),
        "ip_list": check_app["ip_list"],
        "type": type,
        "account": account,
        "script_param": param_content,
        "script_timeout": script_timeout
    }
    result = client.job.fast_execute_script(kwargs)
    if result["result"]:
        time.sleep(5)
        script_result = get_task_ip_log(client, result["data"]["taskInstanceId"], user_name)
        return script_result
    else:
        logger.error(result["message"])
        return ""


def get_task_ip_log(client, task_instance_id, user_name):
    kwargs = {
        "app_code": APP_ID,
        "app_secret": APP_TOKEN,
        "username": user_name,
        "task_instance_id": task_instance_id
    }
    result = client.job.get_task_ip_log(kwargs)
    if result["result"]:
        if result["data"][0]["isFinished"]:
            # return_result = [{"result":False,"ips":''},{"result":True,"ips":''}]
            return_result=[]
            log_content = []
            for i in result["data"][0]["stepAnalyseResult"]:
                if i["resultType"] != 9:
                    logger.error(u"脚本执行失败，错误码如下：")
                    logger.error(i["resultType"])
                    logger.error(i["resultTypeText"])
                    # for a in i["ipLogContent"]:
                    return_result.append({"result":False,"ips":[u["ip"] for u in i["ipLogContent"]]})
                else:
                    log_content += i["ipLogContent"]
                    return_result.append({"result": True, "ips": [u["ip"] for u in i["ipLogContent"]]})
            return return_result
        else:
            import time
            time.sleep(10)
            return get_task_ip_log(client, task_instance_id, user_name)
    else:
        logger.error(result["message"])
        return ""


def set_check_apps(servers):
    server_list = eval(servers)
    app_id_list = []
    for i in server_list:
        if i["app_id"] not in app_id_list:
            app_id_list.append(i["app_id"])
    return_data = []
    for u in app_id_list:
        ip_list = []
        for i in server_list:
            if u == i["app_id"]:
                ip_list.append({"ip": i["ip"], "source": i["source"]})
        return_data.append({"app_id":u,"ip_list":ip_list})
    return return_data





# @periodic_task(run_every=crontab(minute="*/10"))
# def auto_update_business():
#     logger.info(u"开始自动更新业务下的服务器")
#     businesses = Business.objects.all()
#     logger.info(len(businesses))
#     for business in businesses:
#         update_server.delay(business.id, is_update_server=False)


# @task()
# def update_server(business_id, is_update_server=True):
#     logger.info(u"开始更新服务器")
#     try:
#         business = Business.objects.get(id=business_id)
#         username = business.created_by.split(')')[0].split('(')[1]
#         client = get_client_by_user(username)
#         kwargs = {
#             "app_code": APP_ID,
#             "app_secret": APP_TOKEN,
#             "username": username,
#             "app_id": business_id
#         }
#         result = client.cc.get_app_host_list(kwargs)
#         if result["result"]:
#             host_list = result["data"]
#             ip_list = []
#             server_list = Servers.objects.filter(module__business_id=business_id)
#             sql_ip_list = [i.ip for i in server_list]
#             new_ip_list = [i["InnerIP"] for i in host_list]
#             ip_delect = [i for i in sql_ip_list if i not in new_ip_list]
#             for i in ip_delect:
#                 Servers.objects.filter(ip=i).update(is_deleted=True)
#             for host in host_list:
#                 modules = Module.objects.filter(id=host["ModuleID"])
#                 if len(modules) == 0:
#                     module = Module.objects.create(id=host["ModuleID"], name=host["ModuleName"], business=business)
#                 else:
#                     module = modules[0]
#                 servers = Servers.objects.filter(ip=host["InnerIP"])
#                 if len(servers) == 0:
#                     # if host["BakOperator"] =="1":
#                     # if host[""]
#                     Servers.objects.create(module=module, ip=host["InnerIP"], source=host["Source"])
#                 else:
#                     servers.update(is_deleted=False)
#                 server = {"ip": host["InnerIP"], "source": host["Source"]}
#                 if server["source"]:
#                     ip_list.append(server)
#             check_app = {"app_id": business_id, "ip_list": ip_list}
#             if is_update_server:
#                 get_server_info(check_app, username, client)
#         else:
#             logger.error(u"更新业务%s的主机列表失败" % business.name)
#             logger.error(result["messages"])
#
#     except Exception, e:
#         logger.error(e.message)
#
#
# @periodic_task(run_every=crontab(minute=0, hour=0))
# def auto_update_server():
#     businesses = Business.objects.all()
#     for business in businesses:
#         username = business.created_by.split(')')[0].split('(')[1]
#         client = get_client_by_user(username)
#         servers = Servers.objects.filter(module__business_id=business.id, is_deleted=False)
#         ip_list = [{"ip": i.ip, "source": i.source} for i in servers]
#         check_app = {"app_id": business.id, "ip_list": ip_list}
#         get_server_info(check_app, username, client)

#
# def get_server_info(check_app, username, client):
#     script_content = Script_content.objects.get(name="servers_info").content
#     script_result = fast_execute_script(check_app, client, username, script_content, script_timeout=60)
#     logger.info(u"开始获取服务器的操作系统和主机名")
#     if script_result:
#         for log_content in script_result:
#             info = log_content["logContent"]
#             ip = log_content["ip"]
#             info_list = info.split("\n")
#             for server_info in info_list:
#                 new_info = server_info.split("=")
#                 if new_info[0] == "hostname":
#                     Servers.objects.filter(ip=ip).update(host_name=new_info[1])
#                 elif new_info[0] == "operating_system":
#                     Servers.objects.filter(ip=ip).update(operation_system=new_info[1])
#     else:
#         logger.error(u"执行脚本失败，无法获取服务器的操作系统和主机名")
#
#
# @periodic_task(run_every=crontab(minute=0, hour=0))
# def auto_update_server():
#     businesses = Business.objects.all()
#     for business in businesses:
#         username = business.created_by.split(')')[0].split('(')[1]
#         client = get_client_by_user(username)
#         servers = Servers.objects.filter(module__business_id=business.id, is_deleted=False)
#         ip_list = [{"ip": i.ip, "source": i.source} for i in servers]
#         check_app = {"app_id": business.id, "ip_list": ip_list}
#         get_server_info(check_app, username, client)
#


