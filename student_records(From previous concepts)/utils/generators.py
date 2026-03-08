"""
utils/generators.py — Generator Functions
===========================================
Concepts demonstrated:
  - Generator functions with yield
  - Lazy evaluation (generates values on demand, saves memory)
  - Infinite generators with safeguards
  - Batch processing with generators
"""


# ═══════════════════════════════════════════════════════════════
#  ID GENERATOR — Yields unique student IDs
# ═══════════════════════════════════════════════════════════════
def id_generator(prefix="STU", start=1):
    """
    Generator that yields unique student IDs like STU-001, STU-002, ...

    Usage:
        gen = id_generator()
        id1 = next(gen)  # 'STU-001'
        id2 = next(gen)  # 'STU-002'

    Demonstrates:
      - yield keyword (makes this a generator)
      - Lazy evaluation — IDs are generated only when requested
      - Infinite generator — keeps going forever, no list in memory
      - Default parameters
    """
    counter = start
    while True:                         # Infinite loop — generators handle this safely
        yield f"{prefix}-{counter:03d}"  # Format: STU-001, STU-002, etc.
        counter += 1                     # Only increments when next() is called


# ═══════════════════════════════════════════════════════════════
#  BATCH STUDENTS — Yields students in chunks
# ═══════════════════════════════════════════════════════════════
def batch_students(students, batch_size=5):
    """
    Generator that yields students in batches of given size.

    Usage:
        for batch in batch_students(all_students, batch_size=3):
            process(batch)

    Demonstrates:
      - yield with slicing
      - Processing large data in manageable chunks
      - range() with step (batch_size)

    Why generators here?
      - If we have 10,000 students, we don't want to create 2,000
        separate lists in memory. Generator yields one batch at a time.
    """
    for i in range(0, len(students), batch_size):
        yield students[i:i + batch_size]


# ═══════════════════════════════════════════════════════════════
#  MARKS RANGE GENERATOR — Yields students within a marks range
# ═══════════════════════════════════════════════════════════════
def filter_by_marks_range(students, min_marks=0, max_marks=100):
    """
    Generator that yields students whose marks fall within a range.

    Demonstrates:
      - Generator with conditional yield
      - Filtering without creating a new list in memory
    """
    for student in students:
        if min_marks <= student.marks <= max_marks:
            yield student
