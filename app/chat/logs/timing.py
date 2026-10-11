import time
from contextlib import contextmanager

@contextmanager
def timed(name):
    start = time.perf_counter()
    try:
        yield
    finally:
        print(f"[TIMING] {name}: {time.perf_counter() - start:.2f}s", flush=True)