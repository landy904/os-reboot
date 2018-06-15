# -*- coding: utf-8 -*-

from django.conf.urls import patterns

urlpatterns = patterns('home_application.views',
    # 检测管理
    (r'^$', 'home'),
    (r'^sys_management/task_add/', 'task_add_page'),
    (r'^sys_management/task_report/', 'task_report_page'),
    (r'^sys_management/operation_log/', 'operation_log_page'),


    #  执行管理模块
    (r'^create_task/', 'create_task'),
    (r'^modify_task/', 'modify_task'),
    (r'^delete_check_task/', 'delete_check_task'),
    (r'^search_check_task/', 'search_check_task'),
    (r'^get_task_modify_page/', 'get_task_modify_page'),
    #
    # # 系统管理
    # #操作日志模块
    (r'^get_log_list/', 'get_log_list'),
    #
    #
   # 配置平台服务器获取
   (r'^get_sys_tree/', 'get_sys_tree'),
   (r'^get_module_server/', 'get_module_server'),
   #(r'^get_sys_tree_by_ip/', 'get_sys_tree_by_ip'),
   (r'^get_module_by_app_id/', 'get_module_by_appid'),
   (r'^get_server_by_module_id/', 'get_server_by_module_id'),
   (r'^get_select_servers/', 'get_select_servers'),
)
