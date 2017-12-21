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

from django.db import models
from django.utils import timezone


class History(models.Model):
    job_id = models.AutoField(primary_key=True)
    task_id = models.CharField(max_length=10)
    task_name = models.CharField(max_length=50)
    app_id = models.CharField(max_length=10)
    app_name = models.CharField(max_length=50)
    ip = models.CharField(max_length=20)
    user = models.CharField(max_length=20)
    created_date = models.DateTimeField(default=timezone.now)
    totalTime = models.CharField(max_length=10)
    step = models.CharField(max_length=50)

    class Meta:
        db_table = 'history_tab'

    def to_json(self):
        json_data = {}
        json_data['job_id'] = str(self.job_id)
        json_data['task_id'] = self.task_id
        json_data['task_name'] = self.task_name
        json_data['app_id'] = self.app_id
        json_data['app_name'] = self.app_name
        json_data['ip'] = self.ip
        json_data['user'] = self.user
        json_data['created_date'] = str(self.created_date)
        json_data['totalTime'] = self.totalTime
        json_data['step'] = self.step

        return json_data



    def __unicode__(self):
        return self.job_id


class Log(models.Model):
    job_id = models.IntegerField()
    content = models.CharField(max_length=2000)

    class Meta:
        db_table = 'task_log_tab'

    def __unicode__(self):
        return u'{}'.format(self.content[0:50]) or ''
