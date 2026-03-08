# ===== exceptions.py =====
# Custom exception classes for clean error logging


class InvalidRecordError(Exception):
    """Raised when a student record has invalid data."""

    def __init__(self, message):
        self.message = message
        super().__init__(self.message)


class FileLoadError(Exception):
    """Raised when a CSV file cannot be loaded."""

    def __init__(self, message):
        self.message = message
        super().__init__(self.message)


class FineCalculationError(Exception):
    """Raised when there is an error calculating fines."""

    def __init__(self, message):
        self.message = message
        super().__init__(self.message)
