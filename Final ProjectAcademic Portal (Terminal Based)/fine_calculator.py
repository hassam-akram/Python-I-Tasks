# ===== fine_calculator.py =====
# Calculate late fines for overdue fee payments

from exceptions import FineCalculationError
from decorators import log_action, validate_input
from config import FINE_PER_DAY


def calculate_fine(fee_record):
    """Calculate fine for a single fee record."""
    try:
        late_days = fee_record.days_late()
        fine = late_days * FINE_PER_DAY
        return fine
    except Exception as e:
        raise FineCalculationError(f"Error calculating fine for Student {fee_record.student_id}: {e}")


@log_action
@validate_input
def calculate_all_fines(fee_records):
    """Calculate fines for all fee records. Returns list of (student_id, days_late, fine) tuples."""
    fines = []
    for record in fee_records:
        fine = calculate_fine(record)
        fines.append((record.student_id, record.days_late(), fine))

    # Show summary
    total_fines = sum(f[2] for f in fines)
    late_count = sum(1 for f in fines if f[2] > 0)
    print(f"  {late_count} student(s) have late fines.")
    print(f"  Total fines: Rs. {total_fines}")
    return fines
