# -*- coding: utf-8 -*-

from django.db import models


class celery_task_control(models.Model):
    is_stop = models.BooleanField(default=False)
    run_type = models.CharField(max_length=10)
    time = models.CharField(max_length=50, null=True)
    def toDic(self):
        return dict([(attr, getattr(self, attr)) for attr in [f.name for f in self._meta.fields]])

# 执行任务
class Task(models.Model):
    name = models.CharField(max_length=100)
    created_by = models.CharField(max_length=100)
    os_type = models.CharField(max_length=10)
    operation_type = models.CharField(max_length=10)
    task_type = models.CharField(max_length=10)
    servers = models.TextField()
    is_deleted = models.BooleanField(default=False)
    modified_by = models.CharField(max_length=100)
    run_type = models.CharField(max_length=10, default='NOW')
    time_set = models.CharField(max_length=50)
    timer_hour = models.CharField(max_length=50, null=True)
    timer_minu = models.CharField(max_length=50, null=True)
    when_created = models.CharField(max_length=100)
    when_modified = models.CharField(max_length=100)
    celery_task_control = models.OneToOneField(celery_task_control)

    def toDic(self):
        temp_dict = dict(
            [(attr, getattr(self, attr))
             for attr in [f.name for f in self._meta.fields if f.name != "celery_task_control"]])
        temp_dict["celery_task_control"] = self.celery_task_control.toDic()
        return temp_dict


# 操作日志
class Operation_log(models.Model):
    operator = models.CharField(max_length=100, null=True)
    operationtype = models.TextField(max_length=100)
    ostype = models.TextField(max_length=100)
    tasktype = models.TextField(max_length=100)
    operated_detail = models.TextField(max_length=1000)
    when_created = models.CharField(null=True, max_length=100)
    def toDic(self):
        return dict([(attr, getattr(self, attr)) for attr in [f.name for f in self._meta.fields]])



# # Celery 任务时间设置
# class Celery_time_set(models.Model):
#     first_time = models.CharField(max_length=100)
#     run_time = models.CharField(max_length=100)
#     time_interval = models.IntegerField(default=0)
#     set_type = models.CharField(max_length=10)
#     interval_type = models.CharField(max_length=10, default=0)
#     is_deleted = models.BooleanField(default=False)
#
#     def toDic(self):
#         return dict([(attr, getattr(self, attr)) for attr in [f.name for f in self._meta.fields]])
