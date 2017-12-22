# -*- coding: utf-8 -*-
"""
Tencent is pleased to support the open source community by making 蓝鲸智云(BlueKing) available.
Copyright (C) 2017 THL A29 Limited, a Tencent company. All rights reserved.
Licensed under the MIT License (the "License"); you may not use this file except in compliance with the License.
You may obtain a copy of the License at http://opensource.org/licenses/MIT
Unless required by applicable law or agreed to in writing, software distributed under the License is distributed on
an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and limitations under the License.

celery 任务示例

本地启动celery命令: python  manage.py  celery  worker  --settings=settings
周期性任务还需要启动celery调度命令：python  manage.py  celerybeat --settings=settings
"""
import datetime
import time
from celery import task
from celery.schedules import crontab
from celery.task import periodic_task

from common.log import logger
from models import CeleryLog
from blueking.component.shortcuts import get_client_by_request, get_client_by_user


@task()
def async_task(x, y):
    """
    定义一个 celery 异步任务
    """
    logger.error(u"celery 定时任务执行成功，执行结果：{:0>2}:{:0>2}".format(x, y))
    return x + y


def execute_task():
    """
    执行 celery 异步任务

    调用celery任务方法:
        task.delay(arg1, arg2, kwarg1='x', kwarg2='y')
        task.apply_async(args=[arg1, arg2], kwargs={'kwarg1': 'x', 'kwarg2': 'y'})
        delay(): 简便方法，类似调用普通函数
        apply_async(): 设置celery的额外执行选项时必须使用该方法，如定时（eta）等
                      详见 ：http://celery.readthedocs.org/en/latest/userguide/calling.html
    """
    now = datetime.datetime.now()
    logger.error(u"celery 定时任务启动，将在60s后执行，当前时间：{}".format(now))
    # 调用定时任务
    async_task.apply_async(args=[now.hour, now.minute], eta=now + datetime.timedelta(seconds=60))


@periodic_task(run_every=crontab(minute='*/5', hour='*', day_of_week="*"))
def get_time():
    """
    celery 周期任务示例

    run_every=crontab(minute='*/5', hour='*', day_of_week="*")：每 5 分钟执行一次任务
    periodic_task：程序运行时自动触发周期任务
    """
    # execute_task()
    now = datetime.datetime.now()
    print now

def cpu_statistics():
    try:
        app_id = '3'
        task_id = '2'

        data = {'app_id': app_id, 'task_id': task_id}

        client = get_client_by_user('admin')

        stepId=0
        for step in client.job.get_task_detail(data)['data']['nmStepBeanList']:
            stepId=step['stepId']

        steps = [
            {
            'ipList': '1:10.0.1.109,1:10.0.1.220,1:10.0.1.188',
            'stepId': stepId,
            "account": "root",
            },
        ]
        data = {'app_id':app_id, 'task_id': task_id, 'steps': steps}

        execute_result = client.job.execute_task(data)
        task_instance_id = execute_result['data']['taskInstanceId']

        if execute_result['result']:

            is_finished = client.job.get_task_result({'task_instance_id':task_instance_id})['data']['isFinished']
            while not is_finished:
                time.sleep(0.1)
                is_finished = client.job.get_task_result({'task_instance_id': task_instance_id})['data']['isFinished']

        log_contents =  client.job.get_task_ip_log({'task_instance_id': task_instance_id})['data'][0]['stepAnalyseResult'][0]['ipLogContent']

        for log_content in log_contents:
            ip = log_content['ip']
            log = log_content['logContent'].split('all')[1].split('\n')[0]

            celery_log  = CeleryLog.objects.create(
                ip = ip,
                app_id = app_id,
                task_id = task_id,
                log = log,
            )
    except:
        return False

    return True



@periodic_task(run_every=crontab(minute='*/5', hour='*', day_of_week="*"))
def get_cpu_info():
    result = cpu_statistics()

    if result:
        print 'get cpu statistics successfully'
    else:
        print 'get cpu statistics failed'

    now = datetime.datetime.now()
    print now