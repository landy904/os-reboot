# -*- coding: utf-8 -*-

from common.mymako import render_mako_context, render_json
from common.log import logger
from app_control.decorators import function_check
from app_control.models import Function_controller
from account.decorators import *
from home_application.helper import *
from home_application.sys_view import *


def home(request):
    """
    首页
    """
    return render_mako_context(request, '/home_application/sys_management/task_add.html')


def task_add_page(request):
    return render_mako_context(request, '/home_application/sys_management/task_add.html')


def task_report_page(request):
    return render_mako_context(request, '/home_application/sys_management/task_report.html')


def operation_log_page(request):
    return render_mako_context(request, '/home_application/sys_management/operation_log.html')

def get_task_modify_page(request):
    id = request.POST.get("id")
    check_task = get_check_task(id)
    return render_mako_context(request, '/home_application/sys_management/task_modify.html',
                               {"check_task": check_task})

def get_check_task(id):
    check_task = Task.objects.get(id=id)
    return check_task

