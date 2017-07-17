#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Project: tornado-project-template
@File: example.py
@Author: kehr <kehr.china@gmail.com>
@Date: 2017-07-14 16:26:54
@Last Modified by: kehr
@Last Modified time: 2017-07-17 14:20:21
@Description:
"""
import logging
# Tornado 异步处理库
from tornado.gen import coroutine

from base import BaseHandler

class ExampleHandler(BaseHandler):
    """同步处理示例"""
    def get(self):
        self.logger.info('server log.....')
        self.write('Hello World!')


class ExampleAsyncHandler(BaseHandler):
    """异步处理示例"""
    @coroutine
    def get(self):
        result = yield self.async(self.wait, 10)
        self.write('done')

    def wait(self, sec):
        import time
        # logging.info('wait for %s seconds...', sec)
        time.sleep(sec)

