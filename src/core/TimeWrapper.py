import functools
import time


class timeit:
    # A wrapper class for timing method execution using @timeit

    def __init__(self, func):
        functools.update_wrapper(self, func)
        self.func = func

    def __call__(self, *args, **kwargs):
        start_time = time.perf_counter()  # Start timing
        result = self.func(*args, **kwargs)
        end_time = time.perf_counter()  # End timing

        execution_time = (end_time - start_time) * 1000  # Convert to milliseconds
        print(f"{self.func.__name__} executed in {execution_time:.2f} ms")

        return result  # Return the actual function result
