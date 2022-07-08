import logging

from functools import wraps
from typing import Callable


def log(logger_name: str):
    logger = logging.getLogger(logger_name)

    def log_func(route: Callable):

        @wraps(route)
        def wrapper(*args, **kwargs):
            logger.debug('>>>> Entering route with following arguments:')

            for arg in args:
                logger.debug(arg)

            for k, w in kwargs.items():
                logger.debug('{}: {}'.format(k, w))

            response = route(*args, **kwargs)

            logger.debug('<<<< Exiting route with following response:')
            logger.debug('{}'.format(response))

            return response

        return wrapper

    return log_func
