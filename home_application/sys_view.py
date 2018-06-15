# -*- coding: utf-8 -*-

from common.mymako import render_mako_context, render_json
from common.log import logger
from home_application.models import *
from django.db.models import Q
from blueking.component.shortcuts import get_client_by_user
from conf.default import APP_ID, APP_TOKEN
import datetime
from home_application.enums import *
from home_application.celery_tasks import *
from home_application.helper import *

def get_user_name(request):
    return request.user.username

def create_task(request):
    try:
        username=get_user_name(request)
        data = eval(request.POST.get("data"))
        name = data["name"]
        os_type = data["os_type"]
        operation_type = data["operation_type"]
        servers = data["servers"]
        run_type = data["run_type"]
        time_set = data['time_set']
        timer_hour = data['timer_hour']
        timer_minu = data['timer_minu']
        created_by = username
        modified_by = username
        is_deleted = False
        task_type = TASK_STATUS_TYPE.WAITING
        date_now = str(datetime.datetime.now()).split(".")[0]
        task_control = celery_task_control.objects.create(time=time_set, run_type=run_type)
        task_info = Task.objects.create(name=name, os_type=os_type, time_set=time_set, created_by=created_by, run_type=run_type,celery_task_control=task_control,
                                  modified_by=modified_by, operation_type=operation_type, servers=servers,  timer_hour=timer_hour,timer_minu=timer_minu,  when_created=date_now,
                                  when_modified=date_now,  is_deleted=is_deleted,task_type=task_type)
        operator = get_user_name(request)
        if os_type == "L":
            ostype = u"Linux"
        elif os_type == "W":
            ostype = u"Windows"
        if operation_type == "R":
            operationtype = u"重启"
        elif operation_type == "S":
            operationtype = u"关机"
        if run_type == "NOW":
            task_control.is_stop = True
            task_control.save()
            logger.info(u"开始启动任务")
            #run_check_task.delay(username, task_info.id, task_control.id)
            result_data = run_check_task(username, task_info.id, task_control.id)
            operated_detail = u"新增立即执行任务 : " + task_info.name
            tasktype = u"立即"
            insert_log(operator, ostype, operationtype, tasktype, operated_detail)
            return render_json({"is_success": True,"data":run_type,"result_data":result_data})
        elif run_type == "TIMER":
            logger.info(u"开始启动定时任务")
            run_check_task.apply_async(args=[username, task_info.id, task_control.id],
                                       eta=datetime.datetime.strptime(task_control.time, "%Y-%m-%d %H:%M:%S"))
            logger.info(u"启动成功")
            operated_detail = u"新增定时任务 : " + task_info.name
            tasktype = u"定时"
            insert_log(operator, ostype, operationtype, tasktype, operated_detail)
            return render_json({"is_success": True,"data":run_type})
    except Exception, e:
        logger.error(e.message)
        return render_json({"is_success": False, "message": e.message})

def modify_task(request):
    try:
        username = get_user_name(request)
        data = eval(request.POST.get("data"))
        name = data["name"]
        os_type = data["os_type"]
        operation_type = data["operation_type"]
        servers = data["servers"]
        time_set = data['time_set']
        timer_hour = data['timer_hour']
        timer_minu = data['timer_minu']
        modified_by = username
        task_id = data["task_id"]
        old_task = Task.objects.get(id=task_id)
        task_control = old_task.celery_task_control
        is_deleted = False
        task_type = TASK_STATUS_TYPE.WAITING
        date_now = str(datetime.datetime.now()).split(".")[0]
        task_control.time =time_set
        task_control.save()
        old_name = old_task.name
        old_task.name = name
        old_task.os_type = os_type
        old_task.operation_type = operation_type
        old_task.servers = servers
        old_task.time_set = time_set
        old_task.timer_hour = timer_hour
        old_task.timer_minu = timer_minu
        old_task.modified_by = modified_by
        old_task.when_modified = date_now
        old_task.task_type = task_type
        old_task.save()
        logger.info(u"开始启动定时任务")
        run_check_task.apply_async(args=[username, old_task.id, task_control.id],
                                   eta=datetime.datetime.strptime(task_control.time, "%Y-%m-%d %H:%M:%S"))
        logger.info(u"启动成功")
        operator = get_user_name(request)
        if os_type == "L":
            ostype = u"Linux"
        elif os_type == "W":
            ostype = u"Windows"
        if operation_type == "R":
            operationtype = u"重启"
        elif operation_type == "S":
            operationtype = u"关机"
        operated_detail = u"修改定时任务 : " + old_name
        tasktype = u"定时"
        insert_log(operator, ostype, operationtype, tasktype, operated_detail)
        return render_json({"is_success": True})
    except Exception, e:
        logger.error(e.message)
        return render_json({"is_success": False, "message": e.message})



def search_check_task(request):
    try:
        name = request.POST.get("name")
        username= get_user_name(request)
        run_type = "TIMER"
        task_list = Task.objects.filter(name__icontains=name, is_deleted=False,created_by__icontains=username,
                                        celery_task_control__run_type__icontains=run_type).order_by("-when_created")
        return_data = [data.toDic() for data in task_list]
        return render_json({"data": return_data})
    except Exception, e:
        logger.error(e.message)
        return render_json({"is_success": False, "message": e.message})

def delete_check_task(request):
    try:
        id = request.POST.get("id")
        check_task = Task.objects.get(id=id)
        check_task.is_deleted = True
        celery = check_task.celery_task_control
        celery.is_stop = True
        celery.save()
        check_task.save()
        operator = get_user_name(request)
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
        operated_detail = u"删除定时任务 : " + check_task.name
        tasktype = u"定时"
        insert_log(operator, ostype, operationtype, tasktype, operated_detail)
        return render_json({"is_success": True})
    except Exception, e:
        logger.error(e.message)
        return render_json({"is_success": False, "message": e.message})




def get_log_list(request):
    log_operator = request.POST.get("log_operator")
    time_start = str(request.POST.get("time_start"))+" 00:00:00"
    time_end = str(request.POST.get("time_end"))+" 00:00:00"
    try:
        log_content = Operation_log.objects.filter(
            Q(operator__icontains=log_operator) & Q(when_created__range=(time_start, time_end))).order_by(
            "-when_created")
        return_data = [log.toDic() for log in log_content]
        return render_json({'is_success': True, 'data': return_data})
    except Exception, e:
        logger.error(e.message)
        return render_json({"is_success": False, "message": e.message})