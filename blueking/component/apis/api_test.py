# -*- coding: utf-8 -*-
from ..base import ComponentAPI


# 系统组件集合类的名称，一般为 Collections + 系统名
class CollectionsAPITEST(object):

    def __init__(self, client):
        self.client = client

        # create_task为组件名，method为请求组件使用的方法，path为组件路径，组件域名为系统默认域名
        self.api_test = ComponentAPI(
            client=self.client, method='GET', path='/api/c/self-service-api/external_api/call_gims_test/',
            description=u'',
        )

