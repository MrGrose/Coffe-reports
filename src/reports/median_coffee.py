from collections import defaultdict
from collections.abc import Iterable
from statistics import median
from typing import cast

from src.loader.data_loader import Record
from src.reports.base import Report, ReportResult


class MedianCoffeeReport(Report):
    """Отчёт по медианным тратам студентов на кофе."""

    def generate(self, records: Iterable[Record]) -> ReportResult:
        values_by_student = defaultdict(list)

        for record in records:
            values_by_student[record.student].append(record.coffee_spent)

        report_rows = []
        for student, values in values_by_student.items():
            if not values:
                continue
            med_value = median(values)
            report_rows.append([student, med_value])

        report_rows.sort(key=lambda row: cast(float, row[1]), reverse=True)

        headers = ["Студент", "Медианные траты на кофе"]
        return ReportResult(headers=headers, rows=report_rows)
