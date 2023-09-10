import logging
import os


class Logger:
    def __init__(self, logger_name=None):
        if logger_name:
            self.logger = logging.getLogger(logger_name)
        else:
            self.logger = logging.getLogger(self.__class__.__name__)

    def LoggerFactory(self):
        return self.logger

    def debug(self, message):
        self.logger.debug(message)

    def info(self, message):
        self.logger.info(message)

    def error(self, message):
        self.logger.error(message)

    def exception(self, message):
        self.logger.exception(message)

    def critical(self, message):
        self.logger.critical(message)

    def warning(self, message):
        self.logger.warning(message)

    # Configurações do logger
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s.%(msecs)03d | %(levelname)s | %(name)s | %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S',
    )
