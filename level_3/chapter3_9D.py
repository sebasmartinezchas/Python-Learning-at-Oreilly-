import time
from datetime import datetime,timedelta

# Simulate an API that has rate limits
class MockAPI:
    calls_made=[]

    @classmethod
    def make_request(cls,endppoint):
        """Simulate API calls that may fail due to rate limits."""
        cls.calls_made.append(datetime.now())
        #  Check if we made more than 4 calls in the last 10 seconds
        recent_calls=[call for call in cls.calls_made
                                 if call > datetime.now() - timedelta(seconds=10)]
        if len(recent_calls) > 4:
            raise Exception("429 :Rate limit exceeded.")  
        return({"status": "success", "data": f"Response from {endppoint}"})

class RateLimitHandler:
    def __init__(self, max_retries=3,initial_delay=0.5):
        self.max_retries = max_retries
        self.initial_delay = initial_delay
        self.attempt = 0

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        # Handle rate limit exceptions and retry logic
        if exc_type is None:
            return False  # No exception occurred, do not suppress
        
        if '429' in str(exc_value) and self.attempt < self.max_retries:
            delay = self.initial_delay * (2 ** self.attempt)  # Exponential backoff
            print(f"Rate limit hit. Retrying after {delay:.1f} seconds..."
                  f"Attempt {self.attempt + 1} of {self.max_retries}")
            time.sleep(delay)
            return True  # Suppress the exception and retry

        return False  # Propagate the exception if max retries exceeded or not a rate limit error


# Test your implementation with the MockAPI and RateLimitHandler

print("Testing rate limiter with bulk API calls:")
print()
sucessful_calls = 0
endpoints = [f"/users/{i}" for i in range(8)]  # Simulate 8 different endpoints
for endpoint in endpoints: 
    for attempt in range(4):  # Initial call + 3 retries
        
        try:
            with RateLimitHandler(max_retries=3, initial_delay=0.5) as handler:
                handler.attempt = attempt  # Track the current attempt
                response = MockAPI.make_request(endpoint)
                print(f"API call to {endpoint} succeeded: {response}")
                sucessful_calls += 1
                break  # Exit the retry loop on success
        except Exception as e:
                if '429' in str(e) or attempt==3:
                    print(f"API call to {endpoint} failed due to rate limit: {e}")
                else:
                    print(f"API call to {endpoint} failed due to an unexpected error: {e}")
                    break  # Exit the retry loop on unexpected errors

print("\n--- Summary ---")
print(f"\nTotal successful API calls: {sucessful_calls} out of {len(endpoints)}")