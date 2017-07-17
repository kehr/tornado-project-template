# -*- coding: utf-8 -*-
"""
@Project: tornado-project-template
@File: log.py
@Author: kehr <kehr.china@gmail.com>
@Date: 2017-07-17 12:43:42
@Last Modified by: wangkaixuan
@Last Modified time: 2017-07-17 15:19:23
@Description:
"""
import logging
import logging.handlers
import functools

from tornado.log import LogFormatter


DEFAULT_FORMAT = '%(color)s[%(levelname)1.1s %(name)s %(asctime)s '\
                 '%(module)s:%(lineno)d]%(end_color)s %(message)s'
DEFAULT_DATE_FORMAT = '%Y%m%d %H:%M:%S'
BetterFormater = functools.partial(LogFormatter, fmt=DEFAULT_FORMAT, datefmt=DEFAULT_DATE_FORMAT)


def make_logger(name, options):
    """返回项目使用的logger"""
    logger = logging.getLogger(name)
    define_project_logging_options(options, logger)
    return logger


def enable_project_pretty_logging(options=None, logger=None):
    """Turns on formatted logging output as configured.
    """
    if options is None:
        from tornado.options import options
    if options.logging is None or options.logging.lower() == 'none':
        return
    if logger is None:
        logger = logging.getLogger('project')
    logger.setLevel(getattr(logging, options.g_logging_level.upper()))

    # 防止日志被复制到 Tornado log 中
    logger.propagate = False
    if options.g_log_file_prefix:
        rotate_mode = options.g_log_rotate_mode
        if rotate_mode == 'size':
            channel = logging.handlers.RotatingFileHandler(
                filename=options.g_log_file_prefix,
                maxBytes=options.g_log_file_max_size,
                backupCount=options.g_log_file_num_backups)
        elif rotate_mode == 'time':
            channel = logging.handlers.TimedRotatingFileHandler(
                filename=options.g_log_file_prefix,
                when=options.g_log_rotate_when,
                interval=options.g_log_rotate_interval,
                backupCount=options.g_log_file_num_backups)
        else:
            error_message = 'The value of log_rotate_mode option should be ' +\
                            '"size" or "time", not "%s".' % rotate_mode
            raise ValueError(error_message)
        channel.setFormatter(BetterFormater(color=False))
        logger.addHandler(channel)

    if (options.g_log_to_stderr or
            (options.g_log_to_stderr is None and not logger.handlers)):
        # Set up color if we are in a tty and curses is installed
        channel = logging.StreamHandler()
        channel.setFormatter(BetterFormater())
        logger.addHandler(channel)


def define_project_logging_options(options=None, logger=None):
    """为项目日志添加配置"""
    if options is None:
        # late import to prevent cycle
        from tornado.options import options
    options.define('g_logging_level', default='info',
                   help=('Set the Python log level. If \'none\', tornado won\'t touch the '
                         'logging configuration.'),
                   metavar='debug|info|warning|error|none')
    options.define('g_log_file_prefix', type=str, default=None, metavar='PATH',
                   help=('Path prefix for log files. '
                         'Note that if you are running multiple tornado processes, '
                         'log_file_prefix must be different for each of them (e.g. '
                         'include the port number)'))
    options.define('g_log_to_stderr', type=bool, default=None,
                   help=('Send log output to stderr (colorized if possible). '
                         'By default use stderr if --log_file_prefix is not set and '
                         'no other logging is configured.'))
    options.define('g_log_file_max_size', type=int, default=100 * 1000 * 1000,
                   help='max size of log files before rollover')
    options.define('g_log_file_num_backups', type=int, default=10,
                   help='number of log files to keep')

    options.define('g_log_rotate_when', type=str, default='midnight',
                   help=('specify the type of TimedRotatingFileHandler interval '
                         'other options:(\'S\', \'M\', \'H\', \'D\', \'W0\'-\'W6\')'))
    options.define('g_log_rotate_interval', type=int, default=1,
                   help='The interval value of timed rotating')

    options.define('g_log_rotate_mode', type=str, default='size',
                   help='The mode of rotating files(time or size)')

    options.add_parse_callback(lambda: enable_project_pretty_logging(options, logger))
