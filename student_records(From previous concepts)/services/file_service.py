"""
services/file_service.py — File I/O Operations (SRP)
=====================================================
Concepts demonstrated:
  - Single Responsibility Principle — this class ONLY handles file I/O
  - File handling: open(), read, write, with statement
  - JSON: json.dump(), json.load()
  - CSV: csv.writer, csv.DictWriter
  - os module: makedirs, path.exists, path.join
  - datetime for timestamped filenames
  - Exception handling: try/except/finally
"""

import os
import json
import csv
from datetime import datetime

from config.settings import STUDENTS_FILE, EXPORTS_DIR, DATA_PATH
from models.student import Student, GraduateStudent


class FileService:
    """
    Handles all file operations — saving, loading, exporting.
    Follows SRP: only responsible for file I/O, nothing else.
    """

    def __init__(self):
        # Create data directories if they don't exist
        os.makedirs(DATA_PATH, exist_ok=True)
        os.makedirs(EXPORTS_DIR, exist_ok=True)

    # ── JSON Operations ───────────────────────────────────────
    def save_to_json(self, students):
        """
        Save list of Student objects to JSON file.
        Demonstrates: json.dump(), with open(), list comprehension, to_dict()
        """
        try:
            # Convert Student objects to dictionaries using list comprehension
            data = [student.to_dict() for student in students]

            with open(STUDENTS_FILE, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=4, ensure_ascii=False)

            return True

        except IOError as e:
            print(f"  ❌ Error saving file: {e}")
            return False

    def load_from_json(self):
        """
        Load students from JSON file and reconstruct objects.
        Demonstrates: json.load(), file existence check, factory pattern (from_dict)
        """
        # Check if file exists
        if not os.path.exists(STUDENTS_FILE):
            return []  # Return empty list if no data yet

        try:
            with open(STUDENTS_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)

            students = []
            for record in data:
                # Use from_dict class method (factory) based on type
                if record.get("type") == "GraduateStudent":
                    students.append(GraduateStudent.from_dict(record))
                else:
                    students.append(Student.from_dict(record))

            return students

        except json.JSONDecodeError:
            print("  ⚠ Warning: Data file is corrupted. Starting fresh.")
            return []
        except IOError as e:
            print(f"  ❌ Error loading file: {e}")
            return []

    # ── CSV Export ─────────────────────────────────────────────
    def export_to_csv(self, students, filename=None):
        """
        Export students to a timestamped CSV file.
        Demonstrates: csv.DictWriter, datetime formatting, os.path.join
        """
        if not students:
            print("  ⚠ No students to export!")
            return None

        # Generate timestamped filename if not provided
        if filename is None:
            timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
            filename = f"students_export_{timestamp}.csv"

        filepath = os.path.join(EXPORTS_DIR, filename)

        try:
            # Define CSV columns
            fieldnames = ["student_id", "name", "email", "marks",
                          "grade", "subject", "type", "created_at"]

            with open(filepath, "w", newline="", encoding="utf-8") as f:
                writer = csv.DictWriter(f, fieldnames=fieldnames)

                writer.writeheader()  # Write column headers

                for student in students:
                    row = student.to_dict()
                    row["grade"] = Student.grade_from_marks(student.marks)
                    # Remove fields not in fieldnames
                    row = {k: v for k, v in row.items() if k in fieldnames}
                    writer.writerow(row)

            return filepath

        except IOError as e:
            print(f"  ❌ Error exporting CSV: {e}")
            return None

    # ── Read CSV (for verification) ───────────────────────────
    def read_csv(self, filepath):
        """
        Read and display a CSV file.
        Demonstrates: csv.reader, file reading
        """
        try:
            with open(filepath, "r", encoding="utf-8") as f:
                reader = csv.reader(f)
                rows = list(reader)  # Convert to list
            return rows
        except FileNotFoundError:
            print(f"  ❌ File not found: {filepath}")
            return []
        except IOError as e:
            print(f"  ❌ Error reading file: {e}")
            return []

    # ── List Exported Files ───────────────────────────────────
    def list_exports(self):
        """List all exported CSV files. Demonstrates: os.listdir, list comprehension."""
        try:
            files = [f for f in os.listdir(EXPORTS_DIR) if f.endswith(".csv")]
            return files
        except FileNotFoundError:
            return []
