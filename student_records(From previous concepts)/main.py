"""
main.py — Student Records Management System (Entry Point)
============================================================
This is the main entry point for the application.
It wires together ALL modules and provides an interactive CLI menu.

Concepts demonstrated:
  - __name__ == "__main__" guard
  - Procedural paradigm (menu loop, step-by-step flow)
  - Input/output, string formatting (f-strings)
  - Conditionals, while loops
  - Importing from packages (absolute imports)
  - try/except for error handling
  - Calling OOP methods, functional tools, and concurrent operations
"""

# ── Imports from our packages ────────────────────────────────
from config.settings import APP_NAME
from models.student import Student, GraduateStudent
from services.student_service import StudentService
from services.stats_service import StatsService
from services.export_service import ExportService
from utils.validators import (
    StudentNotFoundError,
    InvalidMarksError,
    DuplicateStudentError,
)
from utils.generators import batch_students


# ═══════════════════════════════════════════════════════════════
#  DISPLAY HELPERS — Procedural style
# ═══════════════════════════════════════════════════════════════

def print_header():
    """Display the application header."""
    print("\n" + "=" * 60)
    print(f"  📚  {APP_NAME}")
    print("=" * 60)


def print_menu():
    """Display the main menu."""
    print("\n  ┌─────────────────────────────────────┐")
    print("  │          MAIN MENU                  │")
    print("  ├─────────────────────────────────────┤")
    print("  │  1.  ➕  Add Student                │")
    print("  │  2.  📋  View All Students          │")
    print("  │  3.  🔍  Search Student             │")
    print("  │  4.  ✏️   Update Student             │")
    print("  │  5.  🗑️   Delete Student             │")
    print("  │  6.  📊  Statistics Report          │")
    print("  │  7.  📤  Export Data                 │")
    print("  │  8.  ℹ️   Student Details             │")
    print("  │  0.  🚪  Exit                       │")
    print("  └─────────────────────────────────────┘")


def print_separator():
    print("  " + "-" * 56)


# ═══════════════════════════════════════════════════════════════
#  MENU HANDLERS — Each menu option as a function
# ═══════════════════════════════════════════════════════════════

def handle_add_student(service):
    """Handle adding a new student."""
    print("\n  ➕ ADD NEW STUDENT")
    print_separator()

    try:
        name = input("  Enter name: ").strip()
        email = input("  Enter email: ").strip()
        marks = input("  Enter marks (0-100): ").strip()
        subject = input("  Enter subject [General]: ").strip() or "General"

        # Ask if graduate student
        is_grad = input("  Is this a graduate student? (y/n) [n]: ").strip().lower()
        thesis = "N/A"
        supervisor = "N/A"
        if is_grad == "y":
            thesis = input("  Enter thesis title: ").strip() or "N/A"
            supervisor = input("  Enter supervisor name: ").strip() or "N/A"

        student = service.add_student(
            name=name,
            email=email,
            marks=marks,
            subject=subject,
            is_graduate=(is_grad == "y"),
            thesis_title=thesis,
            supervisor=supervisor,
        )
        print(f"\n  ✅ Student added successfully!")
        print(f"  → {student}")

    except (ValueError, InvalidMarksError, DuplicateStudentError) as e:
        print(f"\n  ❌ Error: {e}")


def handle_view_all(service):
    """Handle viewing all students with formatted table."""
    print("\n  📋 ALL STUDENTS")
    print_separator()

    students = service.get_all_students()
    if not students:
        print("  No students found. Add some first!")
        return

    print(f"  Total: {len(students)} students\n")

    # Table header
    print(f"  {'ID':<10} {'Name':<18} {'Subject':<14} {'Marks':<8} {'Grade':<6} {'Type'}")
    print("  " + "-" * 76)

    # Use batch_students generator to display in batches
    batch_num = 0
    for batch in batch_students(students, batch_size=10):
        for s in batch:
            grade = Student.grade_from_marks(s.marks)
            stype = "Grad" if isinstance(s, GraduateStudent) else "Reg"
            print(f"  {s.student_id:<10} {s.name:<18} {s.subject:<14} {s.marks:<8} {grade:<6} {stype}")
        batch_num += 1


def handle_search(service):
    """Handle searching for students."""
    print("\n  🔍 SEARCH STUDENT")
    print_separator()

    print("  Search by:  1. Name   2. ID")
    choice = input("  Your choice: ").strip()

    try:
        if choice == "1":
            query = input("  Enter name to search: ").strip()
            results = service.search_by_name(query)
            if results:
                print(f"\n  Found {len(results)} result(s):")
                for s in results:
                    print(f"    → {s}")
            else:
                print("  No matching students found.")

        elif choice == "2":
            sid = input("  Enter student ID (e.g., STU-001): ").strip()
            student = service.find_by_id(sid)
            print(f"\n  Found:\n{student.display_info()}")

        else:
            print("  Invalid choice!")

    except StudentNotFoundError as e:
        print(f"\n  ❌ {e}")


def handle_update(service):
    """Handle updating a student's information."""
    print("\n  ✏️  UPDATE STUDENT")
    print_separator()

    sid = input("  Enter student ID to update: ").strip()

    try:
        student = service.find_by_id(sid)
        print(f"  Current info: {student}\n")

        print("  What to update? (leave blank to skip)")
        updates = {}

        new_name = input(f"  Name [{student.name}]: ").strip()
        if new_name:
            updates["name"] = new_name

        new_email = input(f"  Email [{student.email}]: ").strip()
        if new_email:
            updates["email"] = new_email

        new_marks = input(f"  Marks [{student.marks}]: ").strip()
        if new_marks:
            updates["marks"] = new_marks

        new_subject = input(f"  Subject [{student.subject}]: ").strip()
        if new_subject:
            updates["subject"] = new_subject

        if isinstance(student, GraduateStudent):
            new_thesis = input(f"  Thesis [{student.thesis_title}]: ").strip()
            if new_thesis:
                updates["thesis_title"] = new_thesis
            new_supervisor = input(f"  Supervisor [{student.supervisor}]: ").strip()
            if new_supervisor:
                updates["supervisor"] = new_supervisor

        if updates:
            # **kwargs in action! Updates dict is unpacked as keyword arguments
            updated = service.update_student(sid, **updates)
            print(f"\n  ✅ Student updated: {updated}")
        else:
            print("  No changes made.")

    except (StudentNotFoundError, ValueError, InvalidMarksError) as e:
        print(f"\n  ❌ Error: {e}")


def handle_delete(service):
    """Handle deleting a student."""
    print("\n  🗑️  DELETE STUDENT")
    print_separator()

    sid = input("  Enter student ID to delete: ").strip()

    try:
        student = service.find_by_id(sid)
        print(f"  Student to delete: {student}")

        confirm = input("  Are you sure? (y/n): ").strip().lower()
        if confirm == "y":
            # @require_auth decorator will ask for password
            deleted = service.delete_student(sid)
            if deleted:
                print(f"  ✅ Deleted: {deleted}")
        else:
            print("  Cancelled.")

    except StudentNotFoundError as e:
        print(f"\n  ❌ {e}")


def handle_stats(service):
    """Handle viewing statistics report."""
    print("\n  📊 STATISTICS")
    print_separator()

    students = service.get_all_students()
    if not students:
        print("  No students to analyze. Add some first!")
        return

    # Use StatsService (functional paradigm)
    report = StatsService.full_report(students)
    print(report)


def handle_export(service):
    """Handle exporting data using different concurrency models."""
    print("\n  📤 EXPORT DATA")
    print_separator()

    students = service.get_all_students()
    if not students:
        print("  No students to export!")
        return

    export_service = ExportService()

    print("  Export method:")
    print("    1. 🧵 Threaded Export (multiple batches in parallel)")
    print("    2. ⚙️  Multiprocessing Export (CPU-intensive processing)")
    print("    3. ⚡ Async Export (multiple formats simultaneously)")
    print("    4. 📄 Simple CSV Export")

    choice = input("\n  Your choice: ").strip()

    if choice == "1":
        export_service.threaded_export(students)
    elif choice == "2":
        export_service.multiprocess_export(students)
    elif choice == "3":
        export_service.async_export(students)
    elif choice == "4":
        from services.file_service import FileService
        fs = FileService()
        filepath = fs.export_to_csv(students)
        if filepath:
            print(f"\n  ✅ Exported to: {filepath}")
    else:
        print("  Invalid choice!")


def handle_details(service):
    """Handle viewing detailed student information."""
    print("\n  ℹ️  STUDENT DETAILS")
    print_separator()

    sid = input("  Enter student ID: ").strip()

    try:
        student = service.find_by_id(sid)
        print()
        print(student.display_info())  # Polymorphism — different output for Student vs GraduateStudent
        print()

        # Also show __repr__ for demonstration
        print(f"  repr(): {repr(student)}")

    except StudentNotFoundError as e:
        print(f"\n  ❌ {e}")


# ═══════════════════════════════════════════════════════════════
#  MAIN FUNCTION — The Application Loop
# ═══════════════════════════════════════════════════════════════

def main():
    """
    Main application loop — procedural paradigm.
    Wires together OOP services, functional stats, and concurrent exports.
    """
    print_header()

    # Initialize the service (loads existing data from JSON)
    service = StudentService()
    print(f"  📂 Loaded {service.count()} existing student(s)")

    while True:
        print_menu()

        choice = input("\n  Enter your choice (0-8): ").strip()

        if choice == "1":
            handle_add_student(service)
        elif choice == "2":
            handle_view_all(service)
        elif choice == "3":
            handle_search(service)
        elif choice == "4":
            handle_update(service)
        elif choice == "5":
            handle_delete(service)
        elif choice == "6":
            handle_stats(service)
        elif choice == "7":
            handle_export(service)
        elif choice == "8":
            handle_details(service)
        elif choice == "0":
            print("\n  👋 Goodbye! Data has been auto-saved.")
            print("=" * 60 + "\n")
            break
        else:
            print("\n  ⚠ Invalid choice! Please enter 0-8.")


# ═══════════════════════════════════════════════════════════════
#  __name__ == "__main__" GUARD
# ═══════════════════════════════════════════════════════════════
# This ensures main() only runs when this file is executed directly
# (python main.py), NOT when it's imported as a module.

if __name__ == "__main__":
    main()
