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
    def decorator(func):
        cache = {}
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
              # Create a consistent cache key from both positional and keyboard arguments
            cache_key=str(args) + str(sorted(kwargs.items()))
            current_time=datetime.now()
            #Check if a valir, non-expied result exist in the cache
            if cache_key in cache:
                result,timestamp=cache[cache_key]
                if current_time - timestamp < timedelta(seconds=ttl_seconds):
                    print("Cache hit!")
                    return result
            # If no valid cache entry, call the function and update the cache
            print("Cache miss.")
            result=func(*args,**kwargs)
            cache[cache_key]=(result,current_time)
            return result
        return wrapper

    return decorator


# --- Test Code ---
@cache_with_ttl(ttl_seconds=3)
def get_exchange_rate_cached(from_currency, to_currency):
    return get_exchange_rate(from_currency, to_currency)


# ---Test ---
print("First call: ")
rate1=get_exchange_rate_cached("USD","EUR")
print(f"Rate; {rate1:.4f}")
print()

print("Second call (within 3 seconds):")
rate2=get_exchange_rate_cached("USD","EUR")
print(f"Rate: {rate2:.4f}")
print()

print("Waiting for cache to expire...")
time.sleep(4)
print()

print("Third call ( after 4 seconds)")
rate3=get_exchange_rate_cached("USD","EUR")
print(f"Rate: {rate3:.4f}")