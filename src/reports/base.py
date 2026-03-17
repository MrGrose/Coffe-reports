from collections.abc import Iterable
from dataclasses import dataclass
from typing import Protocol

from src.loader.data_loader import Record


@dataclass
class ReportResult:
    """Результат работы отчёта: заголовки и строки таблицы."""

    headers: list[str]
    rows: list[list[object]]


class ReportError(RuntimeError):
    """Базовое исключение для ошибок формирования отчётов."""

    pass


class UnknownReportError(ReportError):
    """Выбрасывается, если запрошен отчёт с неизвестным именем."""

    pass


class Report(Protocol):
    """Интерфейс отчёта."""

    def generate(self, records: Iterable[Record]) -> ReportResult:
        ...
