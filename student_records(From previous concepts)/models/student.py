"""
models/student.py — Student Data Models
=========================================
Concepts demonstrated:
  - Abstract Base Classes (ABC, abstractmethod)
  - Classes, __init__, instance attributes
  - Encapsulation (private attributes + @property)
  - Inheritance (Student → GraduateStudent)
  - Polymorphism (display_info override)
  - Dunder methods (__str__, __repr__, __eq__)
  - Class methods and static methods
  - OCP (Open/Closed Principle) — extend by adding new subclasses
"""

from abc import ABC, abstractmethod
from datetime import datetime


# ═══════════════════════════════════════════════════════════════
#  ABSTRACT BASE CLASS — Person
# ═══════════════════════════════════════════════════════════════
class Person(ABC):
    """
    Abstract base class for all person entities.
    Cannot be instantiated directly — must be subclassed.
    Demonstrates: ABC, @abstractmethod
    """

    def __init__(self, name, email):
        self._name = name        # Encapsulated (protected) attribute
        self._email = email

    # ── Properties (Encapsulation) ────────────────────────────
    @property
    def name(self):
        """Getter for name — controls read access."""
        return self._name

    @name.setter
    def name(self, value):
        """Setter for name — validates before setting."""
        if not value or not value.strip():
            raise ValueError("Name cannot be empty!")
        self._name = value.strip().title()

    @property
    def email(self):
        return self._email

    @email.setter
    def email(self, value):
        if "@" not in value:
            raise ValueError("Invalid email format!")
        self._email = value.strip().lower()

    # ── Abstract Method — must be implemented by subclasses ───
    @abstractmethod
    def display_info(self):
        """Subclasses MUST implement this method."""
        pass

    @abstractmethod
    def to_dict(self):
        """Convert to dictionary for JSON serialization."""
        pass


# ═══════════════════════════════════════════════════════════════
#  STUDENT CLASS — Inherits from Person
# ═══════════════════════════════════════════════════════════════
class Student(Person):
    """
    Represents a regular student.
    Demonstrates: Inheritance, dunder methods, @staticmethod, @classmethod
    """

    def __init__(self, student_id, name, email, marks, subject="General"):
        super().__init__(name, email)     # Call parent constructor
        self._student_id = student_id
        self._marks = marks
        self._subject = subject
        self._created_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # ── Properties ────────────────────────────────────────────
    @property
    def student_id(self):
        return self._student_id

    @property
    def marks(self):
        return self._marks

    @marks.setter
    def marks(self, value):
        if not (0 <= value <= 100):
            raise ValueError("Marks must be between 0 and 100!")
        self._marks = value

    @property
    def subject(self):
        return self._subject

    @subject.setter
    def subject(self, value):
        if not value.strip():
            raise ValueError("Subject cannot be empty!")
        self._subject = value.strip()

    @property
    def created_at(self):
        return self._created_at

    # ── Static Method — doesn't need self or cls ──────────────
    @staticmethod
    def grade_from_marks(marks):
        """
        Calculate grade from marks — pure utility, no instance needed.
        Demonstrates: @staticmethod, conditionals
        """
        if marks >= 90:
            return "A+"
        elif marks >= 80:
            return "A"
        elif marks >= 70:
            return "B"
        elif marks >= 60:
            return "C"
        elif marks >= 50:
            return "D"
        else:
            return "F"

    # ── Class Method — alternative constructor ────────────────
    @classmethod
    def from_dict(cls, data):
        """
        Create a Student from a dictionary.
        Demonstrates: @classmethod as factory method
        """
        student = cls(
            student_id=data["student_id"],
            name=data["name"],
            email=data["email"],
            marks=data["marks"],
            subject=data.get("subject", "General")
        )
        # Restore original creation timestamp if available
        if "created_at" in data:
            student._created_at = data["created_at"]
        return student

    # ── Abstract Method Implementations ───────────────────────
    def display_info(self):
        """Implementation of abstract method — polymorphism."""
        grade = self.grade_from_marks(self._marks)
        return (
            f"  ID      : {self._student_id}\n"
            f"  Name    : {self._name}\n"
            f"  Email   : {self._email}\n"
            f"  Subject : {self._subject}\n"
            f"  Marks   : {self._marks}/100\n"
            f"  Grade   : {grade}\n"
            f"  Added   : {self._created_at}"
        )

    def to_dict(self):
        """Convert student to dictionary for JSON storage."""
        return {
            "type": "Student",
            "student_id": self._student_id,
            "name": self._name,
            "email": self._email,
            "marks": self._marks,
            "subject": self._subject,
            "created_at": self._created_at,
        }

    # ── Dunder Methods ────────────────────────────────────────
    def __str__(self):
        """Human-readable string (print(student) calls this)."""
        grade = self.grade_from_marks(self._marks)
        return f"{self._name} (ID: {self._student_id}) — {self._marks}/100 [{grade}]"

    def __repr__(self):
        """Developer-readable string (useful in debugging)."""
        return f"Student(id={self._student_id!r}, name={self._name!r}, marks={self._marks})"

    def __eq__(self, other):
        """Two students are equal if they have the same ID."""
        if isinstance(other, Student):
            return self._student_id == other._student_id
        return False


# ═══════════════════════════════════════════════════════════════
#  GRADUATE STUDENT — Inherits from Student (OCP: extend, don't modify)
# ═══════════════════════════════════════════════════════════════
class GraduateStudent(Student):
    """
    Extends Student with thesis and supervisor.
    Demonstrates: Multi-level inheritance, polymorphism (overrides display_info),
                  OCP — we added new functionality WITHOUT modifying Student class.
    """

    def __init__(self, student_id, name, email, marks, subject="General",
                 thesis_title="N/A", supervisor="N/A"):
        super().__init__(student_id, name, email, marks, subject)
        self._thesis_title = thesis_title
        self._supervisor = supervisor

    # ── Properties ────────────────────────────────────────────
    @property
    def thesis_title(self):
        return self._thesis_title

    @thesis_title.setter
    def thesis_title(self, value):
        self._thesis_title = value.strip()

    @property
    def supervisor(self):
        return self._supervisor

    @supervisor.setter
    def supervisor(self, value):
        self._supervisor = value.strip()

    # ── Polymorphism — Override display_info ──────────────────
    def display_info(self):
        """Overrides parent's display_info — POLYMORPHISM in action."""
        base_info = super().display_info()
        return (
            f"{base_info}\n"
            f"  Thesis  : {self._thesis_title}\n"
            f"  Advisor : {self._supervisor}"
        )

    def to_dict(self):
        """Extend parent's to_dict with graduate-specific fields."""
        data = super().to_dict()
        data["type"] = "GraduateStudent"
        data["thesis_title"] = self._thesis_title
        data["supervisor"] = self._supervisor
        return data

    @classmethod
    def from_dict(cls, data):
        """Factory method for GraduateStudent."""
        student = cls(
            student_id=data["student_id"],
            name=data["name"],
            email=data["email"],
            marks=data["marks"],
            subject=data.get("subject", "General"),
            thesis_title=data.get("thesis_title", "N/A"),
            supervisor=data.get("supervisor", "N/A"),
        )
        if "created_at" in data:
            student._created_at = data["created_at"]
        return student

    def __str__(self):
        grade = self.grade_from_marks(self._marks)
        return f"{self._name} (ID: {self._student_id}) — {self._marks}/100 [{grade}] [Graduate]"

    def __repr__(self):
        return (f"GraduateStudent(id={self._student_id!r}, name={self._name!r}, "
                f"marks={self._marks}, thesis={self._thesis_title!r})")
