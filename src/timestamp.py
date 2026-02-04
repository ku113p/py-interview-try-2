import time


def get_timestamp() -> float:
    return time.time_ns() / 1_000_000_000
