import logging
import time
from datetime import datetime
from typing import Callable
from functools import wraps

def log(level_name: str) -> Callable:
    level = getattr(logging, level_name.upper(), logging.INFO)
    def decorator(obj):
        if isinstance(obj, type):
            original_init = obj.__init__

            @wraps(original_init)
            def new_init(self, *args, **kwargs):
                logger = logging.getLogger(obj.__name__)
                logger.log(level, "Instantiated %s | args=%s kwargs=%s", obj.__name__, args, kwargs)
                original_init(self, *args, **kwargs)
            obj.__init__ = new_init
            return obj

        @wraps(obj)
        def wrapper(*args, **kwargs):
            start_time = time.perf_counter()
            call_time = datetime.now()

            result = obj(*args, **kwargs)
            duration = time.perf_counter() - start_time

            logger = logging.getLogger(obj.__name__)
            logger.log(level,
                       "\nFunction:  %s\nCall time: %s\nDuration:  %.6fs\nArguments: %s, %s\nResult:    %s",
                       obj.__name__, call_time, duration, args, kwargs, result
                       )
            return result
        return wrapper
    return decorator

