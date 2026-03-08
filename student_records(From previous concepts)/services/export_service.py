"""
services/export_service.py — Concurrent Export Operations
==========================================================
Concepts demonstrated:
  - threading module: Thread, Lock, creating/starting/joining threads
  - Thread safety: race conditions prevented with Lock
  - multiprocessing module: Process, Pool
  - asyncio: async def, await, asyncio.run(), asyncio.gather()
  - GIL (Global Interpreter Lock) — explained in comments
  - Choosing between threads, processes, and async
"""

import threading
import multiprocessing
import asyncio
import time
import csv
import os
from datetime import datetime

from config.settings import EXPORTS_DIR
from models.student import Student
from utils.decorators import timer
from utils.generators import batch_students


class ExportService:
    """
    Handles concurrent export operations using all three concurrency models.
    Demonstrates when to use threads, processes, or async.
    """

    def __init__(self):
        os.makedirs(EXPORTS_DIR, exist_ok=True)
        # Lock for thread safety — prevents race conditions
        self._lock = threading.Lock()
        self._export_count = 0  # Shared counter (needs lock protection!)

    # ══════════════════════════════════════════════════════════
    #  THREADING — Best for I/O-bound tasks
    # ══════════════════════════════════════════════════════════
    # WHY THREADS HERE?
    # File writing is I/O-bound (waiting for disk), so threads work great.
    # The GIL releases during I/O operations, allowing true concurrency.
    # ══════════════════════════════════════════════════════════

    def _write_batch_csv(self, batch, batch_num, filename_prefix):
        """
        Write a batch of students to a CSV file.
        This runs in a separate thread.
        Demonstrates: file I/O in a thread, Lock for shared counter
        """
        filename = f"{filename_prefix}_batch_{batch_num}.csv"
        filepath = os.path.join(EXPORTS_DIR, filename)

        fieldnames = ["student_id", "name", "email", "marks", "grade",
                      "subject", "type", "created_at"]

        with open(filepath, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            for student in batch:
                row = student.to_dict()
                row["grade"] = Student.grade_from_marks(student.marks)
                row = {k: v for k, v in row.items() if k in fieldnames}
                writer.writerow(row)

        # Thread-safe counter update using Lock
        # Without lock, this could cause a RACE CONDITION!
        with self._lock:              # Acquires the lock
            self._export_count += 1   # Safe: only one thread at a time
        # Lock is automatically released here (with statement)

        print(f"    ✅ Thread-{batch_num}: Exported {len(batch)} students → {filename}")

    @timer
    def threaded_export(self, students):
        """
        Export students using multiple threads (one per batch).
        Demonstrates: Thread creation, start, join, batch processing with generators
        """
        if not students:
            print("  ⚠ No students to export!")
            return []

        print("\n  🧵 THREADED EXPORT — Using threading module")
        print("  " + "-" * 50)

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        prefix = f"threaded_{timestamp}"
        self._export_count = 0
        threads = []

        # Use generator to split students into batches
        batch_num = 1
        for batch in batch_students(students, batch_size=3):
            # Create a thread for each batch
            t = threading.Thread(
                target=self._write_batch_csv,
                args=(batch, batch_num, prefix)
            )
            threads.append(t)
            batch_num += 1

        # Start all threads
        for t in threads:
            t.start()

        # Wait for all threads to complete (join)
        for t in threads:
            t.join()

        print(f"\n  📊 Total batches exported: {self._export_count}")
        print(f"  📂 Files saved to: {EXPORTS_DIR}")

        return [f"{prefix}_batch_{i}.csv" for i in range(1, batch_num)]

    # ══════════════════════════════════════════════════════════
    #  MULTIPROCESSING — Best for CPU-bound tasks
    # ══════════════════════════════════════════════════════════
    # WHY MULTIPROCESSING HERE?
    # We simulate CPU-heavy processing (grade calculations, data
    # transformation) on each student. Each process gets its own
    # Python interpreter with its own GIL, so TRUE parallelism
    # is achieved across multiple CPU cores.
    #
    # GIL EXPLANATION:
    # The GIL (Global Interpreter Lock) allows only ONE thread
    # to execute Python bytecode at a time. This means threads
    # DON'T speed up CPU-bound work. Multiprocessing bypasses
    # this limitation by using separate processes (each with its
    # own GIL).
    # ══════════════════════════════════════════════════════════

    @staticmethod
    def _process_student_data(student_dict):
        """
        Process a single student's data (runs in a separate process).
        Must be a static method because process pool requires picklable functions.
        Simulates CPU-heavy processing: multiple calculations per student.
        """
        # Simulate CPU-intensive processing
        marks = student_dict["marks"]
        grade = Student.grade_from_marks(marks)
        percentage = round((marks / 100) * 100, 2)
        gpa = round(marks / 25, 2)
        status = "Pass" if marks >= 50 else "Fail"

        # Return enriched data
        return {
            **student_dict,   # Unpack original data (**kwargs syntax!)
            "grade": grade,
            "percentage": f"{percentage}%",
            "gpa": gpa,
            "status": status,
            "processed_by": f"Process-{os.getpid()}",  # Which process handled it
        }

    @timer
    def multiprocess_export(self, students):
        """
        Process student data using multiprocessing Pool.
        Demonstrates: Pool, pool.map(), Process IDs, pickling
        """
        if not students:
            print("  ⚠ No students to export!")
            return None

        print("\n  ⚙ MULTIPROCESSING EXPORT — Using multiprocessing.Pool")
        print("  " + "-" * 50)

        # Convert students to dicts (Process needs picklable data)
        student_dicts = [s.to_dict() for s in students]

        # Use Pool to distribute work across processes
        # pool.map() splits the data across worker processes
        num_workers = min(4, len(students))  # Max 4 workers
        with multiprocessing.Pool(processes=num_workers) as pool:
            processed_data = pool.map(self._process_student_data, student_dicts)

        # Save processed results to CSV
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"multiprocess_{timestamp}.csv"
        filepath = os.path.join(EXPORTS_DIR, filename)

        if processed_data:
            fieldnames = list(processed_data[0].keys())
            with open(filepath, "w", newline="", encoding="utf-8") as f:
                writer = csv.DictWriter(f, fieldnames=fieldnames)
                writer.writeheader()
                writer.writerows(processed_data)

        print(f"  📊 Processed {len(processed_data)} students across {num_workers} workers")
        print(f"  📂 Saved to: {filename}")

        # Show which process handled each student
        for data in processed_data:
            print(f"    → {data['name']:15s} processed by {data['processed_by']}")

        return filepath

    # ══════════════════════════════════════════════════════════
    #  ASYNCIO — Best for high-volume I/O operations
    # ══════════════════════════════════════════════════════════
    # WHY ASYNC HERE?
    # When exporting to multiple file formats simultaneously,
    # async lets us start all I/O operations without blocking.
    # While one file is being written (I/O wait), another export
    # can start. This is ideal for non-blocking I/O like network
    # requests or file operations.
    # ══════════════════════════════════════════════════════════

    async def _async_export_format(self, students, fmt, timestamp):
        """
        Export students to a specific format asynchronously.
        Demonstrates: async def, await, asyncio.sleep (simulating async I/O)
        """
        filename = f"async_{timestamp}.{fmt}"
        filepath = os.path.join(EXPORTS_DIR, filename)

        print(f"    🔄 Starting {fmt.upper()} export...")

        # Simulate async I/O delay (in real apps, this would be
        # awaiting network requests, database queries, etc.)
        await asyncio.sleep(0.5)

        # Write the file
        if fmt == "csv":
            fieldnames = ["student_id", "name", "email", "marks",
                          "grade", "subject"]
            with open(filepath, "w", newline="", encoding="utf-8") as f:
                writer = csv.DictWriter(f, fieldnames=fieldnames)
                writer.writeheader()
                for s in students:
                    row = s.to_dict()
                    row["grade"] = Student.grade_from_marks(s.marks)
                    row = {k: v for k, v in row.items() if k in fieldnames}
                    writer.writerow(row)

        elif fmt == "txt":
            with open(filepath, "w", encoding="utf-8") as f:
                f.write("STUDENT RECORDS EXPORT\n")
                f.write("=" * 50 + "\n\n")
                for s in students:
                    f.write(f"{s}\n")
                    f.write("-" * 30 + "\n")

        elif fmt == "json":
            import json
            with open(filepath, "w", encoding="utf-8") as f:
                data = [s.to_dict() for s in students]
                json.dump(data, f, indent=2, ensure_ascii=False)

        await asyncio.sleep(0.3)  # Simulated finalization
        print(f"    ✅ {fmt.upper()} export complete → {filename}")
        return filepath

    @timer
    def async_export(self, students):
        """
        Export to multiple formats simultaneously using asyncio.
        Demonstrates: asyncio.run(), asyncio.gather(), async/await
        """
        if not students:
            print("  ⚠ No students to export!")
            return []

        print("\n  ⚡ ASYNC EXPORT — Using asyncio (async/await)")
        print("  " + "-" * 50)

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

        async def run_all_exports():
            """
            Run all format exports concurrently using asyncio.gather().
            gather() starts all coroutines at once and waits for all to finish.
            """
            results = await asyncio.gather(
                self._async_export_format(students, "csv", timestamp),
                self._async_export_format(students, "txt", timestamp),
                self._async_export_format(students, "json", timestamp),
            )
            return results

        # asyncio.run() — the entry point for async code
        filepaths = asyncio.run(run_all_exports())

        print(f"\n  📊 Exported to {len(filepaths)} formats simultaneously!")
        print(f"  📂 Files saved to: {EXPORTS_DIR}")

        return filepaths
