import logging

from settings import settings

get_logger_cls = {}


class ContextFilter(logging.Filter):

    def filter(self, record):
        record.microservice = settings.MICROSERVICE_NAME
        record.file_name = record.filename
        record.function_name = record.funcName
        record.function_line = record.lineno
        return True


class Log:
    level = logging.DEBUG

    def __init__(self):
        self.log_format = ("%(asctime)s | [%(levelname)s] | "
                           "(%(filename)s).%(funcName)s(%(lineno)d) | %(message)s")

    def init(self):
        logger = logging.getLogger(__name__)
        logger.setLevel(self.level)
        logger.addHandler(self.get_stream_handler())
        logger.addFilter(ContextFilter())
        logger.info('--- Инициализации системы логирования ---')
        get_logger_cls['logger'] = logger
        return get_logger_cls.get('logger')

    def get_stream_handler(self):
        stream_handler = logging.StreamHandler()
        stream_handler.setLevel(self.level)
        stream_handler.setFormatter(
            logging.Formatter(
                self.log_format, "%d-%m-%Y %H:%M:%S"
            )
        )
        return stream_handler

    @classmethod
    def get_logger(cls, name) -> logging.Logger:
        self = cls()
        if (logger := get_logger_cls.get('logger')) is None:
            logger = self.init()
        logger.name = name
        return logger
