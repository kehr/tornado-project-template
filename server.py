#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Project: tornado-project-template
@File: server.py
@Author: kehr <kehr.china@gmail.com>
@Date: 2017-07-14 16:11:34
@Last Modified by: wangkaixuan
@Last Modified time: 2017-07-17 17:15:19
@Description:
"""

import sys
reload(sys)
sys.setdefaultencoding('utf-8')

import os
import socket
import json
import tornado.web
import tornado.ioloop
import tornado.options
import tornado.httpserver

from lib.log import make_logger
from tornado.options import define
from tornado.options import options

# 所有的处理请求的 Handler 引入
from lib.handler.example import ExampleHandler
from lib.handler.example import ExampleAsyncHandler

# 如果有额外的参数在这里添加
define('port', default=8000, help='server port, default is 8000', type=int)


class Application(tornado.web.Application):
    """服务器设置"""
    def __init__(self):
        self.project_path = os.path.dirname(os.path.realpath(__file__))
        self.hostname = socket.gethostname()
        self.hostip = socket.gethostbyname(self.hostname)
        self.logger = make_logger('server', options)

        # 注册所有的路由
        handlers = [
            (r'/', ExampleHandler),
            (r'/example/async', ExampleAsyncHandler),
        ]

        settings = {
            'static_path': os.path.join(self.project_path, 'static'),
            'debug': True
        }

        self._init_environment()
        super(Application, self).__init__(handlers, **settings)

    def _init_environment(self):
        """初始化服务器环境"""
        self.prepare_dirs(['log'])
        tornado.options.parse_config_file('conf/tornado.conf')
        # parse_command_line 和 parse_config_file 不能同时使用
        # 会重复添加处理日志的 Handler
        # tornado.options.parse_command_line()

    def prepare_dirs(self, dirs):
        """创建数据目录"""
        for d in dirs:
            if not os.path.exists(d):
                self.logger.warn('Dir[%s] does not exists. create it.', d)
                os.makedirs(d)


if __name__ == '__main__':
    tornado.httpserver.HTTPServer(Application()).listen(options.port)
    tornado.ioloop.IOLoop.instance().start()




