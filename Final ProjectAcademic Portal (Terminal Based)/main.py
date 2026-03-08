# ===== main.py =====
# Terminal menu and entry point for the Academic Portal

import asyncio
from data_loader import load_all_data
from validators import validate_students, get_failed_students
from fine_calculator import calculate_all_fines
from report_generator import generate_report


# ---------- Global state ----------
students = []
fees = []
valid_students = []
failed_students = []
fines = []
data_loaded = False


# ---------- Menu Functions ----------

async def load_data():
    """Load and validate all data from CSV files."""
    global students, fees, valid_students, failed_students, fines, data_loaded

    # Step 1: Load CSV files concurrently
    result = await load_all_data("data/students.csv", "data/fees.csv")

    if result is None:
        print("  Failed to load data. Check your CSV files.")
        return

    students, fees = result

    # Step 2: Validate student records
    valid_students = validate_students(students)

    if valid_students is None:
        valid_students = []

    # Step 3: Flag failed students
    failed_students = get_failed_students(valid_students)

    # Step 4: Calculate fines
    fines = calculate_all_fines(fees)

    if fines is None:
        fines = []

    data_loaded = True
    print("\n  All data loaded and processed successfully!")


def show_all_students():
    """Display all valid students."""
    if not data_loaded:
        print("\n  Please load data first (Option 1).\n")
        return

    print("\n" + "=" * 60)
    print("  ALL VALID STUDENTS")
    print("=" * 60)
    for s in valid_students:
        print(f"  {s}")
    print(f"\n  Total: {len(valid_students)} student(s)")
    print("=" * 60)


def show_failed_students():
    """Display failed students."""
    if not data_loaded:
        print("\n  Please load data first (Option 1).\n")
        return

    print("\n" + "=" * 60)
    print("  FAILED STUDENTS")
    print("=" * 60)
    if failed_students:
        for s in failed_students:
            print(f"  {s}")
    else:
        print("  No failed students found.")
    print(f"\n  Total Failed: {len(failed_students)} student(s)")
    print("=" * 60)


def show_fines():
    """Display late fines."""
    if not data_loaded:
        print("\n  Please load data first (Option 1).\n")
        return

    print("\n" + "=" * 60)
    print("  LATE FINES")
    print("=" * 60)
    any_fine = False
    for student_id, days_late, fine in fines:
        if fine > 0:
            print(f"  Student {student_id}: {days_late} days late — Fine: Rs. {fine}")
            any_fine = True
    if not any_fine:
        print("  No late fines.")
    total = sum(f[2] for f in fines)
    print(f"\n  Total Fines: Rs. {total}")
    print("=" * 60)


def create_report():
    """Generate a timestamped report."""
    if not data_loaded:
        print("\n  Please load data first (Option 1).\n")
        return

    generate_report(valid_students, failed_students, fines)


# ---------- Main Menu ----------

async def main():
    """Main terminal menu loop."""
    print("\n" + "=" * 60)
    print("   ACADEMIC PORTAL — Student Records System")
    print("=" * 60)

    while True:
        print("\n  ---- MENU ----")
        print("  1. Load & Validate Data")
        print("  2. Show All Students")
        print("  3. Show Failed Students")
        print("  4. Show Late Fines")
        print("  5. Generate Report")
        print("  6. Exit")

        choice = input("\n  Enter your choice (1-6): ").strip()

        if choice == "1":
            await load_data()
        elif choice == "2":
            show_all_students()
        elif choice == "3":
            show_failed_students()
        elif choice == "4":
            show_fines()
        elif choice == "5":
            create_report()
        elif choice == "6":
            print("\n  Goodbye!\n")
            break
        else:
            print("\n  Invalid choice. Please enter 1-6.")


# ---------- Entry Point ----------
if __name__ == "__main__":
    asyncio.run(main())
