from functools import wraps
from typing import Iterable, Callable, Any, Optional, Type
import time
import logging


logger = logging.getLogger(__name__)


def backoff(exceptions: Optional[Iterable[Type[Exception]]] = None,
            start_sleep_time: float = 0.1,
            factor: int = 2,
            border_sleep_time: int = 10) -> Callable:

    def func_wrapper(func: Callable) -> Callable:
        nonlocal exceptions

        iteration = 0
        prev_sleep_time = 0
        exceptions = exceptions or (Exception,)

        @wraps(func)
        def inner(*args, **kwargs) -> Any:
            nonlocal iteration
            nonlocal prev_sleep_time
            nonlocal exceptions
            try:
                return func(*args, **kwargs)
            except Exception as e:
                if not isinstance(e, exceptions):
                    raise e
                time_to_sleep = min(border_sleep_time, start_sleep_time * factor ** (iteration))
                logger.debug(f"Couldn't process function {func.__name__}, due to: {e}. Iteration: {iteration}, sleep: {time_to_sleep}")
                if prev_sleep_time == border_sleep_time:
                    raise e
                prev_sleep_time = time_to_sleep
                iteration += 1
                time.sleep(time_to_sleep)
                return inner(*args, **kwargs)

        return inner

    return func_wrapper
