# ===== models.py =====
# OOP classes for Student and FeeRecord

from datetime import datetime


class Student:
    """Represents a student record."""

    def __init__(self, student_id, name, marks, enrollment_date):
        self.student_id = student_id
        self.name = name
        self.marks = marks
        self.enrollment_date = enrollment_date

    def is_passed(self, pass_marks):
        """Check if student passed based on pass marks threshold."""
        return self.marks >= pass_marks

    def __str__(self):
        status = "PASS" if self.marks >= 50 else "FAIL"
        return f"ID: {self.student_id} | Name: {self.name} | Marks: {self.marks} | Enrolled: {self.enrollment_date} | {status}"


class FeeRecord:
    """Represents a fee payment record."""

    def __init__(self, student_id, amount, due_date, paid_date):
        self.student_id = student_id
        self.amount = amount
        self.due_date = due_date
        self.paid_date = paid_date

    def days_late(self):
        """Calculate how many days late the payment was."""
        if self.paid_date <= self.due_date:
            return 0
        delta = self.paid_date - self.due_date
        return delta.days

    def __str__(self):
        late = self.days_late()
        late_text = f"{late} days late" if late > 0 else "On time"
        return f"Student ID: {self.student_id} | Amount: {self.amount} | Due: {self.due_date} | Paid: {self.paid_date} | {late_text}"
