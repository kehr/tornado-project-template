#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Project: tornado-project-template
@File: base.py
@Author: kehr <kehr.china@gmail.com>
@Date: 2017-07-17 13:40:40
@Last Modified by: wangkaixuan
@Last Modified time: 2017-07-17 15:06:24
@Description:
"""

import os
import time
import socket
import functools
import threading
import tornado.web

from tornado.options import options
from tornado.web import StaticFileHandler
from tornado.concurrent import Future
from tornado.options import options


class BaseHandler(tornado.web.RequestHandler):
    """公共基础类"""
    def write_error(self, status_code, **kwargs):
        """Handle http error"""
        if 404 == status_code:
            self.write('File not found')
        else:
            super(BaseHandler, self).write_error(status_code, **kwargs)

    def initialize(self):
        """initialize"""
        self.response = {}
        self.project_path = self.application.project_path
        self.logger = self.application.logger

    def get_file_server_path(self, path, **kwargs):
        return '{}://{}:{}/{}'.format(self.request.protocol,
                                      socket.gethostname(), options.port, path)

    def async(self, func, *args, **kwargs):
        """异步调用"""
        return self.thread_async(func, *args, **kwargs)
        #return self.ioloop_async(func, *args, **kwargs)

    def ioloop_async(self, func, *args, **kwargs):
        """基于 IOLoop 的异步调度"""
        future = Future()
        @functools.wraps(func)
        def _wrapper(*args, **kwargs):
            try:
                result = func(*args, **kwargs)
                if isinstance(result, Future):
                    result = result.result()
            except Exception as e:
                result = None
                future.set_exception(e)
            future.set_result(result)
        tornado.ioloop.IOLoop.current().add_callback(functools.partial(_wrapper, *args, **kwargs))
        return future

    def thread_async(self, func, *args, **kwargs):
        """基于线程的异步调用"""
        future = Future()
        @functools.wraps(func)
        def _wrapper():
            try:
                result = func(*args, **kwargs)
                # 如果异步调用中再次开了多个异步调用
                # 则需要解析多个异步调用的 Future 结果
                if isinstance(result, Future):
                    result = result.result()
                future.set_result(result)
            except Exception as e:
                future.set_exception(e)
                self.logger.exception(e)

        t = threading.Thread(target=_wrapper)
        t.daemon = True
        t.start()
        return future


def cost(func):
    """计算函数执行时间
    如果该函数是类成员，则输出类名和函数名；
    如果函数不属于类，则出书函数名称
    """
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        """wrapper"""
        func_start = time.time()
        result = func(*args, **kwargs)
        func_cost = '{0:.4f} ms'.format((time.time() - func_start) * 1000)
        if hasattr(args[0], '__class__'):
            logging.debug('%s:%s cost time: %s',
                args[0].__class__.__name__, func.__name__, func_cost)
        else:
            logging.debug('%s cost time: %s', func.__name__, func_cost)
        return result
    return wrapper
