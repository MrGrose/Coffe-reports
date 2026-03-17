from collections.abc import Callable

from src.reports.base import Report, UnknownReportError
from src.reports.median_coffee import MedianCoffeeReport

ReportFactory = Callable[[], Report]


_REPORTS: dict[str, ReportFactory] = {
    "median-coffee": MedianCoffeeReport,
}


def get_available_reports() -> list[str]:
    """Возвращает отсортированный список доступных имён отчётов."""
    return sorted(_REPORTS)


def get_report(name: str) -> Report:
    """Возвращает экземпляр отчёта по его имени или выбрасывает ошибку."""
    factory = _REPORTS.get(name.strip())
    if factory is None:
        available = get_available_reports() or ["отчёты отсутствуют"]
        raise UnknownReportError(
            f"Неизвестный отчёт: '{name.strip()}'. "
            f"Доступные отчёты: {', '.join(available)}."
        )
    return factory()
