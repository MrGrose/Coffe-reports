import csv
from collections.abc import Iterable
from dataclasses import dataclass
from pathlib import Path


class DataLoadError(RuntimeError):
    pass


@dataclass
class Record:
    """Структура записи о тратах студента на кофе."""

    student: str
    coffee_spent: int


def _validate_path(path: Path) -> None:
    """Проверяет существование и тип пути к файлу."""

    if not path.exists():
        raise DataLoadError(f"Файл не найден: {path}")
    if not path.is_file():
        raise DataLoadError(f"Путь не является файлом: {path}")


def _validate_header(reader: csv.DictReader, path: Path) -> None:
    """Проверяет наличие обязательных столбцов в CSV-файле."""

    if not reader.fieldnames:
        raise DataLoadError(f"Файл {path} не содержит заголовок столбцов.")

    required_fields = {"student", "coffee_spent"}
    present = {name.strip() for name in reader.fieldnames if name}
    missing = required_fields.difference(present)
    if missing:
        missing_str = ", ".join(sorted(missing))
        raise DataLoadError(
            f"В файле {path} отсутствуют обязательные столбцы: {missing_str}."
        )


def _parse_record_row(row: dict[str, str]) -> Record | None:
    """Разбирает одну строку CSV в Record.

    Плохие или неполные строки пропускаются вместо выброса исключения.
    """

    student = (row.get("student", "")).strip()
    coffee_raw = (row.get("coffee_spent", "")).strip()

    if not (student and coffee_raw):
        return None

    try:
        coffee_spent = int(coffee_raw)
    except ValueError:
        return None

    return Record(student=student, coffee_spent=coffee_spent)


def _load_records_from_file(path: Path) -> list[Record]:
    """Загружает и валидирует записи из одного CSV-файла."""

    _validate_path(path)

    try:
        with path.open("r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            _validate_header(reader, path)

            records: list[Record] = []
            for row in reader:
                if record := _parse_record_row(row):
                    records.append(record)
    except OSError as exc:
        raise DataLoadError(f"Ошибка при чтении файла: {path}") from exc

    return records


def load_records(paths: Iterable[str | Path]) -> list[Record]:
    """Загружает записи из нескольких CSV-файлов."""

    all_records: list[Record] = []

    for raw_path in paths:
        path = Path(raw_path)
        all_records.extend(_load_records_from_file(path))

    return all_records
