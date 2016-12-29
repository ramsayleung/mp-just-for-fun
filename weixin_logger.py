import logging


class WeixinLogger(object):
    def __init__(self, name):
        self.logger_name = name

    def get_logger(self):
        logger = logging.getLogger(self.logger_name)
        logger.setLevel(logging.INFO)

        # create a file handler
        handler = logging.FileHandler('{}.log'.format(self.logger_name))
        handler.setLevel(logging.WARNING)

        # create a logging format
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)

        # add the handlers to the logger
        logger.addHandler(handler)

        return logger
