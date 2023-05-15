from functools import wraps
import time
import logging


logger = logging.getLogger(__name__)


def backoff(start_sleep_time=0.1, factor=2, border_sleep_time=10):

    def func_wrapper(func):

        iteration = 0
        prev_sleep_time = 0

        @wraps(func)
        def inner(*args, **kwargs):
            nonlocal iteration
            nonlocal prev_sleep_time
            try:
                return func(*args, **kwargs)
            except Exception as e:
                logger.debug(f"Couldn't process function {func.__name__}, due to: {e}.")
                if prev_sleep_time == border_sleep_time:
                    raise e
                time_to_sleep = min(border_sleep_time, start_sleep_time * factor ** (iteration))
                prev_sleep_time = time_to_sleep
                iteration += 1
                time.sleep(time_to_sleep)
                return inner(*args, **kwargs)

        return inner

    return func_wrapper
