from src.loader.data_loader import Record
from src.reports.base import UnknownReportError
from src.utils.registry import get_report
from src.reports.median_coffee import MedianCoffeeReport


def test_median_coffee_report_calculates_median_and_sorts() -> None:
    records = [
        Record(student="А", coffee_spent=100),
        Record(student="А", coffee_spent=300),
        Record(student="Б", coffee_spent=200),
        Record(student="Б", coffee_spent=400),
        Record(student="В", coffee_spent=50),
    ]

    report = MedianCoffeeReport()
    result = report.generate(records)

    assert result.headers == ["Студент", "Медианные траты на кофе"]
    assert result.rows == [
        ["Б", 300],
        ["А", 200],
        ["В", 50],
    ]


def test_median_coffee_report_empty_records() -> None:
    report = MedianCoffeeReport()
    result = report.generate([])

    assert result.headers == ["Студент", "Медианные траты на кофе"]
    assert result.rows == []


def test_get_report_unknown_name() -> None:
    name = "unknown-report"
    try:
        get_report(name)
    except UnknownReportError as exc:
        assert "Неизвестный отчёт" in str(exc)
        assert name in str(exc)
    else:
        raise AssertionError("Ожидалось исключение UnknownReportError")
