"""
services/student_service.py — CRUD Operations (SRP)
=====================================================
Concepts demonstrated:
  - Single Responsibility Principle — ONLY handles student CRUD
  - Procedural + OOP paradigm mix
  - Custom exceptions (raise and catch)
  - Decorators applied to methods
  - Generator usage (id_generator)
  - List operations, loops, conditionals
"""

from models.student import Student, GraduateStudent
from services.file_service import FileService
from utils.validators import (
    StudentNotFoundError,
    DuplicateStudentError,
    validate_name,
    validate_email,
    validate_marks,
    validate_subject,
)
from utils.decorators import log_action, require_auth
from utils.generators import id_generator


class StudentService:
    """
    Manages student CRUD operations.
    Follows SRP: only responsible for student data management.
    """

    def __init__(self):
        self.file_service = FileService()
        self.students = self.file_service.load_from_json()

        # Initialize the ID generator — start after the highest existing ID
        highest_id = self._get_highest_id()
        self._id_gen = id_generator(prefix="STU", start=highest_id + 1)

    def _get_highest_id(self):
        """Find the highest student ID number to continue from."""
        if not self.students:
            return 0
        max_num = 0
        for s in self.students:
            try:
                num = int(s.student_id.split("-")[1])
                if num > max_num:
                    max_num = num
            except (IndexError, ValueError):
                continue
        return max_num

    def _save(self):
        """Save current students list to file."""
        self.file_service.save_to_json(self.students)

    # ── CREATE ────────────────────────────────────────────────
    @log_action
    def add_student(self, name, email, marks, subject="General",
                    is_graduate=False, thesis_title="N/A", supervisor="N/A"):
        """
        Add a new student. Validates input and checks for duplicates.
        Demonstrates: decorators, validation, generators (next()), exceptions
        """
        # Validate inputs (raises exceptions if invalid)
        name = validate_name(name)
        email = validate_email(email)
        marks = validate_marks(marks)
        subject = validate_subject(subject)

        # Check for duplicate email
        for s in self.students:
            if s.email == email:
                raise DuplicateStudentError(email)

        # Generate unique ID using generator
        student_id = next(self._id_gen)   # <-- Generator in action!

        # Create appropriate student type (Polymorphism/OCP)
        if is_graduate:
            student = GraduateStudent(
                student_id=student_id,
                name=name,
                email=email,
                marks=marks,
                subject=subject,
                thesis_title=thesis_title,
                supervisor=supervisor,
            )
        else:
            student = Student(
                student_id=student_id,
                name=name,
                email=email,
                marks=marks,
                subject=subject,
            )

        self.students.append(student)
        self._save()
        return student

    # ── READ ──────────────────────────────────────────────────
    def get_all_students(self):
        """Return all students. Simple and clean."""
        return self.students

    def find_by_id(self, student_id):
        """
        Find student by ID.
        Demonstrates: loop + conditional, custom exception
        """
        for student in self.students:
            if student.student_id == student_id.upper():
                return student
        raise StudentNotFoundError(student_id)

    def search_by_name(self, name_query):
        """
        Search students by name (partial match).
        Demonstrates: list comprehension with condition, string methods
        """
        query = name_query.lower().strip()
        results = [s for s in self.students if query in s.name.lower()]
        return results

    # ── UPDATE ────────────────────────────────────────────────
    @log_action
    def update_student(self, student_id, **kwargs):
        """
        Update student fields.
        Demonstrates: **kwargs (keyword arguments), property setters, decorators
        """
        student = self.find_by_id(student_id)

        # Update fields using **kwargs
        if "name" in kwargs:
            student.name = validate_name(kwargs["name"])
        if "email" in kwargs:
            student.email = validate_email(kwargs["email"])
        if "marks" in kwargs:
            student.marks = validate_marks(kwargs["marks"])
        if "subject" in kwargs:
            student.subject = validate_subject(kwargs["subject"])

        # Graduate-specific fields
        if isinstance(student, GraduateStudent):
            if "thesis_title" in kwargs:
                student.thesis_title = kwargs["thesis_title"]
            if "supervisor" in kwargs:
                student.supervisor = kwargs["supervisor"]

        self._save()
        return student

    # ── DELETE ────────────────────────────────────────────────
    @require_auth                     # <-- Must enter admin password!
    @log_action
    def delete_student(self, student_id):
        """
        Delete a student by ID.
        Demonstrates: decorator stacking (@require_auth + @log_action)
        """
        student = self.find_by_id(student_id)
        self.students.remove(student)
        self._save()
        return student

    # ── UTILITY ───────────────────────────────────────────────
    def count(self):
        """Return total number of students."""
        return len(self.students)
