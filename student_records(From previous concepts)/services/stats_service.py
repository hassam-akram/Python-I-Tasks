"""
services/stats_service.py — Statistical Analysis (Functional Paradigm)
=======================================================================
Concepts demonstrated:
  - Functional programming paradigm (pure functions, no side effects)
  - lambda expressions
  - map(), filter(), reduce()
  - List comprehensions and dict comprehensions
  - sorted() with key parameter
  - math module
"""

from functools import reduce
import math

from models.student import Student


class StatsService:
    """
    Calculates statistics using FUNCTIONAL paradigm.
    All methods are essentially pure functions — they take data and return results
    without modifying the original data.
    """

    # ── Average Marks — using reduce + lambda ─────────────────
    @staticmethod
    def average_marks(students):
        """
        Calculate average marks using reduce() and lambda.
        Demonstrates: reduce(), lambda, ternary operator
        """
        if not students:
            return 0

        # reduce(function, iterable, initial_value)
        # lambda takes accumulator and current item
        total = reduce(lambda acc, s: acc + s.marks, students, 0)
        return round(total / len(students), 2)

    # ── Highest & Lowest — using max/min with key=lambda ──────
    @staticmethod
    def highest_scorer(students):
        """Find student with highest marks using max() + lambda."""
        if not students:
            return None
        return max(students, key=lambda s: s.marks)

    @staticmethod
    def lowest_scorer(students):
        """Find student with lowest marks using min() + lambda."""
        if not students:
            return None
        return min(students, key=lambda s: s.marks)

    # ── Get Toppers — using filter + lambda ───────────────────
    @staticmethod
    def get_toppers(students, threshold=80):
        """
        Get students scoring above threshold.
        Demonstrates: filter() + lambda
        """
        toppers = list(filter(lambda s: s.marks >= threshold, students))
        return toppers

    # ── Get Failing — using filter + lambda ───────────────────
    @staticmethod
    def get_failing(students, pass_marks=50):
        """Get students below passing marks using filter()."""
        return list(filter(lambda s: s.marks < pass_marks, students))

    # ── Grade Distribution — using dict comprehension ─────────
    @staticmethod
    def grade_distribution(students):
        """
        Count students in each grade category.
        Demonstrates: dict comprehension, map(), Counter-like logic
        """
        if not students:
            return {}

        # Use map() to get all grades
        grades = list(map(lambda s: Student.grade_from_marks(s.marks), students))

        # Count grades using dict comprehension
        distribution = {grade: grades.count(grade) for grade in set(grades)}

        # Sort by grade order
        grade_order = ["A+", "A", "B", "C", "D", "F"]
        sorted_dist = {g: distribution.get(g, 0) for g in grade_order if g in distribution}

        return sorted_dist

    # ── Subject-wise Average — using comprehensions ───────────
    @staticmethod
    def subject_averages(students):
        """
        Calculate average marks per subject.
        Demonstrates: dict comprehension, list comprehension, set comprehension
        """
        if not students:
            return {}

        # Get unique subjects using set comprehension
        subjects = {s.subject for s in students}

        # Calculate average for each subject
        averages = {}
        for subject in subjects:
            # List comprehension to filter marks for this subject
            subject_marks = [s.marks for s in students if s.subject == subject]
            averages[subject] = round(sum(subject_marks) / len(subject_marks), 2)

        return averages

    # ── Sorted Students — using sorted + lambda ──────────────
    @staticmethod
    def sorted_by_marks(students, reverse=True):
        """
        Return students sorted by marks.
        Demonstrates: sorted() with key=lambda, reverse parameter
        """
        return sorted(students, key=lambda s: s.marks, reverse=reverse)

    # ── Names List — using map ────────────────────────────────
    @staticmethod
    def get_all_names(students):
        """
        Get list of all student names.
        Demonstrates: map() to transform data
        """
        return list(map(lambda s: s.name, students))

    # ── Standard Deviation — using math module ────────────────
    @staticmethod
    def std_deviation(students):
        """
        Calculate standard deviation of marks.
        Demonstrates: math module (math.sqrt), functional approach
        """
        if len(students) < 2:
            return 0

        avg = StatsService.average_marks(students)

        # Variance using map + lambda + reduce
        squared_diffs = list(map(lambda s: (s.marks - avg) ** 2, students))
        variance = reduce(lambda acc, x: acc + x, squared_diffs, 0) / len(students)

        return round(math.sqrt(variance), 2)

    # ── Full Report — combines all stats ──────────────────────
    @staticmethod
    def full_report(students):
        """Generate a complete statistics report."""
        if not students:
            return "No students to analyze."

        avg = StatsService.average_marks(students)
        highest = StatsService.highest_scorer(students)
        lowest = StatsService.lowest_scorer(students)
        toppers = StatsService.get_toppers(students)
        failing = StatsService.get_failing(students)
        grades = StatsService.grade_distribution(students)
        subj_avg = StatsService.subject_averages(students)
        std_dev = StatsService.std_deviation(students)

        report = []
        report.append("=" * 60)
        report.append("         STUDENT STATISTICS REPORT")
        report.append("=" * 60)
        report.append(f"  Total Students  : {len(students)}")
        report.append(f"  Average Marks   : {avg}/100")
        report.append(f"  Std Deviation   : {std_dev}")
        report.append(f"  Highest Scorer  : {highest.name} ({highest.marks}/100)")
        report.append(f"  Lowest Scorer   : {lowest.name} ({lowest.marks}/100)")
        report.append(f"  Toppers (80+)   : {len(toppers)}")
        report.append(f"  Failing (<50)   : {len(failing)}")
        report.append("-" * 60)

        # Grade Distribution
        report.append("  Grade Distribution:")
        for grade, count in grades.items():
            bar = "█" * count
            report.append(f"    {grade:3s} : {bar} ({count})")

        report.append("-" * 60)

        # Subject Averages
        report.append("  Subject-wise Averages:")
        for subject, avg_m in subj_avg.items():
            report.append(f"    {subject:20s} : {avg_m}/100")

        report.append("=" * 60)

        return "\n".join(report)
