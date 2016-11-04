import logging


class MyLoggger(object):
    @staticmethod
    def initialize(app_name):
        logger = logging.getLogger(app_name)
        if not getattr(logger, 'handler_set', None):
            logger.setLevel(logging.INFO)
            filename = app_name+'_logs.log'
            file_handler = logging.FileHandler(filename)
            formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
            file_handler.setFormatter(formatter)
            logger.addHandler(file_handler)
            logger.handler_set = True
        return logger

    @staticmethod
    def close(logger):
        logger