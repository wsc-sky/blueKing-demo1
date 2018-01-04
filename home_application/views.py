# -*- coding: utf-8 -*-
"""
Tencent is pleased to support the open source community by making 蓝鲸智云(BlueKing) available.
Copyright (C) 2017 THL A29 Limited, a Tencent company. All rights reserved.
Licensed under the MIT License (the "License"); you may not use this file except in compliance with the License.
You may obtain a copy of the License at http://opensource.org/licenses/MIT
Unless required by applicable law or agreed to in writing, software distributed under the License is distributed on
an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and limitations under the License.
"""

from common.mymako import render_mako_context, render_json
from blueking.component.shortcuts import get_client_by_request, get_client_by_user
from .models import History, Log, CeleryLog
import time


def home(request):
    user = request.user.username

    client = get_client_by_request(request)
    a = client.cc.get_app_by_user()
    app_list = client.cc.get_app_by_user()['data']

    data = {'app_id': '12'}
    task_list = [] if client.job.get_task(data)['data'] == None else client.job.get_task(data)['data']

    host_list = client.cc.get_app_host_list({'app_id': '12'})['data']

    return render_mako_context(request, '/home_application/home.mako',
                               {'app_list': app_list, 'task_list': task_list, 'host_list': host_list})


def get_task_by_app(request, app_id=None):
    user = request.user.username
    data = {'app_id': app_id}
    client = get_client_by_request(request)
    task_list = client.job.get_task(data)['data']

    return render_json({'task_list': task_list})


def get_host_by_app(request, app_id=None):
    user = request.user.username
    data = {'app_id': app_id}
    client = get_client_by_request(request)
    host_list = client.cc.get_app_host_list(data)['data']

    return render_json({'host_list': host_list})


def execute_task(request):
    user = request.user.username

    ip = request.POST['ip']

    post_data = request.POST

    app_id = post_data['app_id']
    app_name = post_data['app_name']
    task_id = post_data['task_id']
    task_name = post_data['task_name']

    data = {'app_id': app_id, 'task_id': task_id}

    client = get_client_by_request(request)

    stepId = 0
    for step in client.job.get_task_detail(data)['data']['nmStepBeanList']:
        stepId = step['stepId']

    steps = [{
        'ipList': '1:' + ip,
        'stepId': stepId,
        "account": "root",

    }]
    data = {'app_id': app_id, 'task_id': task_id, 'steps': steps}

    execute_result = client.job.execute_task(data)

    task_instance_id = execute_result['data']['taskInstanceId']

    if execute_result['result']:

        is_finished = client.job.get_task_result({'task_instance_id': task_instance_id})['data']['isFinished']
        while not is_finished:
            time.sleep(0.1)
            is_finished = client.job.get_task_result({'task_instance_id': task_instance_id})['data']['isFinished']

        logData = client.job.get_task_ip_log({'task_instance_id': task_instance_id})['data'][0]['stepAnalyseResult'][0][
            'ipLogContent'][0]
        totalTime = logData['totalTime']
        log = logData['logContent']
        len_of_log = len(log)

        if len_of_log > 1999:
            log = log[len_of_log - 1999:len_of_log]
        history = History.objects.create(
            task_id=task_id,
            task_name=task_name,
            app_id='3',
            app_name=app_name,
            ip=ip,
            user=user,
            totalTime=str(totalTime)[0:5],
            step=str(stepId),
        )
        log = Log.objects.create(
            job_id=history.job_id,
            content=log,
        )

    return render_json({'execute_result': execute_result})


def get_task_log(request, job_id):
    log = Log.objects.get(job_id=job_id)

    return render_json({'log': log.content})


def filter_history(request):
    get_data = request.GET
    user = get_data['user']
    app_id = get_data['app_id']
    task_id = get_data['task_id']

    history_list = History.objects

    if user != 'all':
        history_list = History.objects.filter(user=user)
    if app_id != 'all':
        history_list = history_list.filter(app_id=app_id)
    if task_id != 'all':
        history_list = history_list.filter(task_id=task_id)

    result_list = [history.to_json() for history in history_list.order_by('-created_date')]

    return render_json({'history_list': result_list})


def dev_guide(request):
    """
    开发指引
    """
    return render_mako_context(request, '/home_application/dev_guide.html')


def contactus(request):
    """
    联系我们
    """
    return render_mako_context(request, '/home_application/contact.html')


def result_page(request):
    user = request.user.username

    clientAdmin = get_client_by_request(request)

    user_list = clientAdmin.bk_login.get_all_user()['data']

    client = get_client_by_request(request)
    app_list = client.cc.get_app_by_user()['data']

    data = {'app_id': '3'}
    task_list = [] if client.job.get_task(data)['data'] == None else client.job.get_task(data)['data']

    history_data = History.objects.all().order_by('-created_date')

    history_list = [history.to_json() for history in history_data]

    return render_mako_context(request, '/task_result/result.html',
                               {'user_list': user_list, 'app_list': app_list, 'task_list': task_list,
                                'history_list': history_list})


def cpu_statistics_page(request):
    return render_mako_context(request, '/cpu_usage_rate_statistics/cpu_statistics.html', {})


def get_cpu_statistics(request):
    ip = request.GET['ip']
    celery_history = CeleryLog.objects.filter(ip=ip).order_by('-created_date')[0:10][::-1]

    data = {}

    data['code'] = 0
    data['result'] = True,
    data['message'] = 'success'
    data['data'] = {}
    data['data']['xAxis'] = []
    data['data']['series'] = []
    time = celery_history[9].created_date.minute + celery_history[0].created_date.hour * 60

    user_usage_json = {'name': 'User Usage', 'type': 'line', 'data': []}
    sys_usage_json = {'name': 'System Usage', 'type': 'line', 'data': []}
    all_usage_json = {'name': 'Idle', 'type': 'line', 'data': []}

    for history in celery_history:
        data['data']['xAxis'].append(str(time / 60) + ":" + str(time - (time / 60) * 60))
        time -= 5
        log = filter(None, history.log.split(' '))
        user_usage = str(log[0]).strip()
        sys_usage = log[2]
        all_usage = log[9]
        user_usage_json['data'].append(float(user_usage))
        sys_usage_json['data'].append(float(sys_usage))
        all_usage_json['data'].append(float(all_usage))

    data['data']['series'].append(user_usage_json)
    data['data']['series'].append(sys_usage_json)
    data['data']['series'].append(all_usage_json)

    data['data']['xAxis'] = data['data']['xAxis'][::-1]
    return render_json(data)


def get_app_by_user(request):
    user = request.user.username

    client = get_client_by_request(request)

    app_list = client.cc.get_app_by_user()['data']

    print render_json({'app_list': app_list})


###### test functon ######


def test(request):
    user = request.user.username

    client = get_client_by_request(request)

    result = client.external_api.api_test()

    return render_json({'success':result})

def admin_page(request):
    return render_mako_context(request, '/admin/admin_page.html')