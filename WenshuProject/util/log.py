# coding:utf-8
import logging
import logging.config as log_conf
import os

current_dir = os.path.dirname(os.path.realpath(__file__))
log_dir = os.path.dirname(current_dir)


def get_logfile(file):
    log_dir = os.path.dirname(current_dir) + "/logs"
    logfile = os.path.join(log_dir, file)
    return logfile


log_config = {
    'version': 1.0,
    'formatters': {
        'detail': {
            'format': '%(asctime)s - %(filename)s[line:%(lineno)d] - %(name)s - %(levelname)s - %(message)s',
            'datefmt': "%Y-%m-%d %H:%M:%S"
        },
        'simple': {
            'format': '%(name)s - %(levelname)s - %(message)s',
        },
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'level': 'DEBUG',
            'formatter': 'detail'
        },
        'rotatingFileBySize': {
            'class': 'logging.handlers.RotatingFileHandler',
            'maxBytes': 1024 * 1024 * 5,
            'backupCount': 10,
            'filename': get_logfile("detail.log"),
            'level': 'DEBUG',
            'formatter': 'detail',
            'encoding': 'utf-8',
        },
        'rotatingFileByTime': {
            'class': 'logging.handlers.TimedRotatingFileHandler',
            'interval': 1,
            'when': 'D',
            'backupCount': 10,
            'filename': get_logfile("tax.log"),
            'level': 'DEBUG',
            'formatter': 'detail',
            'encoding': 'utf-8',

        },
        'spider_error': {
            'class': 'logging.handlers.TimedRotatingFileHandler',
            'interval': 1,
            'when': 'D',
            'backupCount': 10,
            'filename': get_logfile("error.log"),
            'level': 'DEBUG',
            'formatter': 'detail',
            'encoding': 'utf-8',

        },
        'storage_page': {
            'class': 'logging.handlers.TimedRotatingFileHandler',
            'interval': 1,
            'when': 'D',
            'backupCount': 10,
            'filename': get_logfile("page.log"),
            'level': 'DEBUG',
            'formatter': 'detail',
            'encoding': 'utf-8',
        }
    },
    'loggers': {
        'crawler': {
            'handlers': ['console', 'rotatingFileByTime'],
            'level': 'DEBUG',
        },
        'parser': {
            'handlers': ['console', 'rotatingFileByTime'],
            'level': 'DEBUG',
        },
        'other': {
            'handlers': ['console', 'rotatingFileByTime'],
            'level': 'DEBUG',
        },
        'detail': {
            'handlers': ['console', 'rotatingFileBySize'],
            'level': 'DEBUG',
        },
        'error': {
            'handlers': ['console', 'spider_error'],
            'level': 'DEBUG',
        },
        'page': {
            'handlers': ['console', 'storage_page'],
            'level': 'DEBUG',
        }
    }
}

log_conf.dictConfig(log_config)

other = logging.getLogger('other')
crawler = logging.getLogger('crawler')
parser = logging.getLogger('page_parser')
detail = logging.getLogger('detail')
error = logging.getLogger('error')
page = logging.getLogger("page")

__all__ = ['crawler', 'parser', 'other', 'detail', 'error', 'page']

if __name__ == '__main__':
    page.info("dddddddddddd")
