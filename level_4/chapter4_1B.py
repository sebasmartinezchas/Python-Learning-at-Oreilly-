import time
import functools
import logging

logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")


def log_with_level(level="INFO"):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            logging.log(
                logging.getLevelNamesMapping()[level],
                f"Calling '{func.__name__}' with args {args}kwargs{kwargs}",
            )
            result = func(*args, **kwargs)
            logging.log(
                logging.getLevelNamesMapping()[level],
                f"'{func.__name__}' returned {result}",
            )
            return result

        return wrapper

    return decorator


@log_with_level(level="INFO")
def process_user_data(user_id, action="view"):
    """Simulate processing user data."""
    time.sleep(0.1)
    return f"Processed {action} for user {user_id}"


process_user_data(42, action="edit")
