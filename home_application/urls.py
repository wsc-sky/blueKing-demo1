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

from django.conf.urls import patterns

urlpatterns = patterns(
    'home_application.views',

    ##### page ####
    (r'^$', 'home'),
    (r'^dev-guide/$', 'dev_guide'),
    (r'^contactus/$', 'contactus'),
    (r'^history/$', 'result_page'),
    (r'^cpu_chart/$', 'cpu_statistics_page'),
    (r'^admin-page/$', 'admin_page'),

    ##### API method ######
    (r'^get_task_by_app/(?P<app_id>\w+)/$', 'get_task_by_app'),
    (r'^get_host_by_app/(?P<app_id>\w+)/$', 'get_host_by_app'),
    (r'^get_app_by_user/$', 'get_app_by_user'),
    (r'^execute_task/$', 'execute_task'),
    (r'^filter_history/$', 'filter_history'),
    (r'^get_task_log/(?P<job_id>\w+)/$', 'get_task_log'),
    (r'^get_cpu_statistics/$', 'get_cpu_statistics'),

    ####  method test #####
    (r'^test/$', 'test'),

)
