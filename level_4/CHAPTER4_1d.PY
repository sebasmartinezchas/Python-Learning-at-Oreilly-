import time
import random
import functools
from datetime import datetime, timedelta


def get_exchange_rate(from_currency, to_currency):
    """Simulate an expensie API call to get exchange rates."""
    print(f"---- Making expensive API call from {from_currency} to {to_currency}")
    time.sleep(0.5)
    base_rates = {"USD_EUR": 0.93, "USD_GBP": 0.81, "EUR_GBP": 0.87}
    rate = base_rates.get(f"{from_currency}_{to_currency}", 1.0)
    return rate + random.uniform(-0.01, 0.01)


# Your task is to implement this decorator!
def cache_with_ttl(ttl_seconds=60):
    """
    Your decorator should:
    1 . Accept a `ttl_seconds` parameter.
    2 . Cache function result using arguments as the cache key.
    3 . Return a cached result if i't not expired
    4 . Call the function and refresh the cache if the result is expired or not found.
    5 . Preserve the original function's metadata.

    """

    # Your implementation here
    def decorator(func):
        cache = {}

        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            currency_pair = args
            time_now = time.time()
            if currency_pair in cache:
                cached_result, cached_time = cache[currency_pair]
                if time_now - cached_time < ttl_seconds:

                    return cached_result
            result = func(*args, **kwargs)
            cache[currency_pair] = (result, time_now)
            return result

        return wrapper

    return decorator


# --- Test Code ---
@cache_with_ttl(ttl_seconds=3)
def get_exchange_rate_cached(from_currency, to_currency):
    return get_exchange_rate(from_currency, to_currency)


# ---Test ---
print(get_exchange_rate_cached("USD", "EUR"))
print(get_exchange_rate_cached("USD", "EUR"))
time.sleep(4)
print(get_exchange_rate_cached("USD", "EUR"))
