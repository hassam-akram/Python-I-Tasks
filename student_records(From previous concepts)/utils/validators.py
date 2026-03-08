"""
utils/validators.py — Input Validation & Custom Exceptions
============================================================
Concepts demonstrated:
  - Custom exception classes (inheriting from Exception)
  - Exception hierarchy
  - raise keyword
  - Input validation functions
  - String methods for validation
"""


# ═══════════════════════════════════════════════════════════════
#  CUSTOM EXCEPTIONS — Exception hierarchy
# ═══════════════════════════════════════════════════════════════

class StudentRecordError(Exception):
    """Base exception for all student record errors."""
    pass


class StudentNotFoundError(StudentRecordError):
    """Raised when a student is not found by ID or name."""

    def __init__(self, identifier):
        self.identifier = identifier
        super().__init__(f"Student not found: '{identifier}'")


class InvalidMarksError(StudentRecordError):
    """Raised when marks are not in valid range (0-100)."""

    def __init__(self, marks):
        self.marks = marks
        super().__init__(f"Invalid marks: {marks}. Must be between 0 and 100.")


class DuplicateStudentError(StudentRecordError):
    """Raised when trying to add a student with an existing ID."""

    def __init__(self, student_id):
        self.student_id = student_id
        super().__init__(f"Student with ID '{student_id}' already exists!")


class AuthenticationError(StudentRecordError):
    """Raised when admin password is incorrect."""

    def __init__(self):
        super().__init__("Authentication failed! Incorrect password.")


# ═══════════════════════════════════════════════════════════════
#  VALIDATION FUNCTIONS
# ═══════════════════════════════════════════════════════════════

def validate_name(name):
    """
    Validate student name.
    - Must not be empty
    - Must contain only letters and spaces
    Returns cleaned name or raises ValueError.
    """
    if not name or not name.strip():
        raise ValueError("Name cannot be empty!")

    cleaned = name.strip()
    # Allow letters, spaces, and dots (for names like "Dr. Ali")
    if not all(c.isalpha() or c in (" ", ".") for c in cleaned):
        raise ValueError("Name must contain only letters, spaces, and dots!")

    return cleaned.title()


def validate_email(email):
    """
    Simple email validation.
    - Must contain @ symbol
    - Must have text before and after @
    - Must have a dot after @
    """
    if not email or not email.strip():
        raise ValueError("Email cannot be empty!")

    email = email.strip().lower()

    if "@" not in email:
        raise ValueError("Email must contain '@' symbol!")

    parts = email.split("@")
    if len(parts) != 2 or not parts[0] or not parts[1]:
        raise ValueError("Invalid email format!")

    if "." not in parts[1]:
        raise ValueError("Email domain must contain a dot (e.g., .com)!")

    return email


def validate_marks(marks_input):
    """
    Validate and convert marks input.
    - Must be a number
    - Must be between 0 and 100
    Returns integer marks or raises InvalidMarksError.
    """
    try:
        marks = float(marks_input)
        marks = int(round(marks))
    except (ValueError, TypeError):
        raise InvalidMarksError(marks_input)

    if not (0 <= marks <= 100):
        raise InvalidMarksError(marks)

    return marks


def validate_subject(subject):
    """Validate subject name — must not be empty."""
    if not subject or not subject.strip():
        raise ValueError("Subject cannot be empty!")
    return subject.strip().title()
