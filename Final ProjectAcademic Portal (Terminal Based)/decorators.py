# ===== decorators.py =====
# Decorators for logging and error handling

from datetime import datetime
from functools import wraps


def log_action(func):
    """Decorator that logs start and end of a function with timestamp."""

    @wraps(func)
    def wrapper(*args, **kwargs):
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f"\n[{now}] Starting '{func.__name__}'...")
        result = func(*args, **kwargs)
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f"[{now}] Finished '{func.__name__}'.\n")
        return result

    return wrapper


def validate_input(func):
    """Decorator that wraps function in try-except for clean error logging."""

    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            print(f"[{now}] ERROR in '{func.__name__}': {type(e).__name__}: {e}")
            return None

    return wrapper
