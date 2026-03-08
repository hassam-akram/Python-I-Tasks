# ===== validators.py =====
# Validate student records and flag failed students

from exceptions import InvalidRecordError
from decorators import log_action, validate_input
from config import PASS_MARKS


@log_action
@validate_input
def validate_students(students):
    """Validate each student record. Returns list of valid students."""
    valid_students = []
    invalid_count = 0

    for student in students:
        try:
            # Check if name is empty
            if not student.name:
                raise InvalidRecordError(f"Student ID {student.student_id}: Name is empty.")

            # Check if marks are in valid range (0 to 100)
            if student.marks < 0 or student.marks > 100:
                raise InvalidRecordError(f"Student ID {student.student_id}: Marks {student.marks} out of range (0-100).")

            # Record is valid
            valid_students.append(student)

        except InvalidRecordError as e:
            print(f"  [INVALID] {e.message}")
            invalid_count += 1

    print(f"\n  Valid Records: {len(valid_students)}")
    print(f"  Invalid Records: {invalid_count}")
    return valid_students


@log_action
def get_failed_students(students):
    """Filter and return students who failed (marks < PASS_MARKS)."""
    failed = [s for s in students if not s.is_passed(PASS_MARKS)]
    print(f"  Found {len(failed)} failed student(s) (marks < {PASS_MARKS}).")
    return failed
