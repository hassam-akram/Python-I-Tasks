# ===== report_generator.py =====
# Generate timestamped text reports

import os
from datetime import datetime
from decorators import log_action, validate_input
from config import REPORT_DIR


@log_action
@validate_input
def generate_report(students, failed_students, fines):
    """Generate a timestamped report file in the reports/ directory."""

    # Create reports directory if it doesn't exist
    os.makedirs(REPORT_DIR, exist_ok=True)

    # Create timestamped filename
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"report_{timestamp}.txt"
    filepath = os.path.join(REPORT_DIR, filename)

    with open(filepath, "w") as file:

        file.write("=" * 60 + "\n")
        file.write("       ACADEMIC PORTAL — STUDENT REPORT\n")
        file.write(f"       Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        file.write("=" * 60 + "\n\n")

        # --- All Students ---
        file.write("-" * 60 + "\n")
        file.write("  ALL STUDENTS\n")
        file.write("-" * 60 + "\n")
        for s in students:
            file.write(f"  {s}\n")
        file.write(f"\n  Total Students: {len(students)}\n\n")

        # --- Failed Students ---
        file.write("-" * 60 + "\n")
        file.write("  FAILED STUDENTS\n")
        file.write("-" * 60 + "\n")
        if failed_students:
            for s in failed_students:
                file.write(f"  {s}\n")
        else:
            file.write("  No failed students.\n")
        file.write(f"\n  Total Failed: {len(failed_students)}\n\n")

        # --- Late Fines ---
        file.write("-" * 60 + "\n")
        file.write("  LATE FINES\n")
        file.write("-" * 60 + "\n")
        total_fines = 0
        for student_id, days_late, fine in fines:
            if fine > 0:
                file.write(f"  Student {student_id}: {days_late} days late — Fine: Rs. {fine}\n")
                total_fines += fine
        if total_fines == 0:
            file.write("  No late fines.\n")
        file.write(f"\n  Total Fines: Rs. {total_fines}\n")
        file.write("\n" + "=" * 60 + "\n")

    print(f"  Report saved to: {filepath}")
    return filepath
