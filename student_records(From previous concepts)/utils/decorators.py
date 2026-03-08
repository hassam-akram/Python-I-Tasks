"""
utils/decorators.py — Reusable Decorators
==========================================
Concepts demonstrated:
  - Decorators (functions that wrap other functions)
  - Closures (inner functions accessing outer scope)
  - *args, **kwargs (accepting any arguments)
  - functools.wraps (preserving original function metadata)
  - datetime for timestamps
"""

import time
import functools
from datetime import datetime
from config.settings import ADMIN_PASSWORD


# ═══════════════════════════════════════════════════════════════
#  @log_action — Logs every function call with timestamp
# ═══════════════════════════════════════════════════════════════
def log_action(func):
    """
    Decorator that logs when a function is called and what it returns.

    Usage:
        @log_action
        def add_student(name): ...

    Demonstrates: decorator, closure, *args/**kwargs, functools.wraps
    """
    @functools.wraps(func)         # Preserves original function's name and docstring
    def wrapper(*args, **kwargs):  # *args/**kwargs — accept ANY arguments
        timestamp = datetime.now().strftime("%H:%M:%S")
        print(f"  [{timestamp}] Calling: {func.__name__}()")

        result = func(*args, **kwargs)  # Call the original function

        print(f"  [{timestamp}] Completed: {func.__name__}()")
        return result
    return wrapper


# ═══════════════════════════════════════════════════════════════
#  @timer — Measures execution time
# ═══════════════════════════════════════════════════════════════
def timer(func):
    """
    Decorator that measures how long a function takes to execute.

    Usage:
        @timer
        def process_data(): ...

    Demonstrates: decorator, time module, f-string formatting
    """
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.time()           # Start timer

        result = func(*args, **kwargs)     # Run the function

        end_time = time.time()             # End timer
        elapsed = end_time - start_time
        print(f"  ⏱ {func.__name__}() took {elapsed:.4f} seconds")
        return result
    return wrapper


# ═══════════════════════════════════════════════════════════════
#  @require_auth — Asks for admin password before running
# ═══════════════════════════════════════════════════════════════
def require_auth(func):
    """
    Decorator that prompts for admin password before executing.
    Only allows the function to run if the correct password is entered.

    Usage:
        @require_auth
        def delete_student(id): ...

    Demonstrates: decorator with control flow, environment variables
    """
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        print("\n  🔒 This action requires admin authentication.")
        password = input("  Enter admin password: ").strip()

        if password == ADMIN_PASSWORD:
            print("  ✅ Authentication successful!\n")
            return func(*args, **kwargs)
        else:
            print("  ❌ Wrong password! Action denied.\n")
            return None
    return wrapper
