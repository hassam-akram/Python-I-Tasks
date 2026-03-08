# ===== data_loader.py =====
# Async CSV loading using asyncio

import csv
import asyncio
from datetime import datetime
from models import Student, FeeRecord
from exceptions import FileLoadError
from decorators import log_action, validate_input


def _read_students_csv(filepath):
    """Read students CSV file and return list of Student objects."""
    try:
        students = []
        with open(filepath, "r") as file:
            reader = csv.DictReader(file)
            for row in reader:
                student = Student(
                    student_id=int(row["id"]),
                    name=row["name"].strip(),
                    marks=int(row["marks"]),
                    enrollment_date=datetime.strptime(row["enrollment_date"], "%Y-%m-%d").date()
                )
                students.append(student)
        return students
    except FileNotFoundError:
        raise FileLoadError(f"File not found: {filepath}")
    except Exception as e:
        raise FileLoadError(f"Error reading {filepath}: {e}")


def _read_fees_csv(filepath):
    """Read fees CSV file and return list of FeeRecord objects."""
    try:
        fees = []
        with open(filepath, "r") as file:
            reader = csv.DictReader(file)
            for row in reader:
                fee = FeeRecord(
                    student_id=int(row["student_id"]),
                    amount=int(row["amount"]),
                    due_date=datetime.strptime(row["due_date"], "%Y-%m-%d").date(),
                    paid_date=datetime.strptime(row["paid_date"], "%Y-%m-%d").date()
                )
                fees.append(fee)
        return fees
    except FileNotFoundError:
        raise FileLoadError(f"File not found: {filepath}")
    except Exception as e:
        raise FileLoadError(f"Error reading {filepath}: {e}")


async def load_students(filepath):
    """Async wrapper — loads students CSV in a separate thread."""
    return await asyncio.to_thread(_read_students_csv, filepath)


async def load_fees(filepath):
    """Async wrapper — loads fees CSV in a separate thread."""
    return await asyncio.to_thread(_read_fees_csv, filepath)


@log_action
@validate_input
async def load_all_data(students_path, fees_path):
    """Load both CSV files concurrently using asyncio.gather()."""
    students, fees = await asyncio.gather(
        load_students(students_path),
        load_fees(fees_path)
    )
    print(f"  Loaded {len(students)} student records.")
    print(f"  Loaded {len(fees)} fee records.")
    return students, fees
