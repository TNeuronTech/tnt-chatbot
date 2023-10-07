# Copyright (c) TNeuron Technology
# All rights reserved.
#
# This source code's license can be found in the
# LICENSE file in the root directory of this source tree.

from loguru import logger as loguru_logger

from tntchatbot.config.settings import settings

class Logger:

    # def __init__(self, name='app_logger', log_file='app.log', level=logging.DEBUG):
    def __init__(self):
        # self.logger = logging.getLogger(name)
        # self.logger.setLevel(level)

        # # Create a file handler and set the logging level
        # file_handler = logging.FileHandler(log_file)
        # file_handler.setLevel(level)

        # # Create a formatter and set the format for log messages
        # formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        # file_handler.setFormatter(formatter)

        # # Add the file handler to the logger
        # self.logger.addHandler(file_handler)

        loguru_logger.add(
            settings.LOG_FILE_NAME,
            rotation=settings.LOG_ROTATION,
            retention=settings.LOG_RETENTION,
            format=settings.LOG_FORMAT, 
            filter=settings.LOG_FILTER, 
            level=settings.LOG_LEVEL,
            colorize=True)
        self.logger = loguru_logger

    def get_logger(self):
        return self.logger

logger = Logger().get_logger()