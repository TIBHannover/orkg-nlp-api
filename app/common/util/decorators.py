import logging

from functools import wraps
from typing import Callable


def log(logger_name: str):
    logger = logging.getLogger(logger_name)

    def log_func(route: Callable):

        @wraps(route)
        def wrapper(*args, **kwargs):
            logger.info('>>>> Entering route with following arguments:')

            for arg in args:
                logger.info(arg)

            for k, w in kwargs.items():
                logger.info('{}: {}'.format(k, w))

            response = route(*args, **kwargs)

            logger.info('<<<< Exiting route with following response:')
            logger.info('{}'.format(response))

            return response

        return wrapper

    return log_func
