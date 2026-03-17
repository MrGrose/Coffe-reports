from pathlib import Path

import pytest
from src.loader.data_loader import DataLoadError, Record, load_records


def test_load_records_from_single_file(tmp_path: Path) -> None:
    csv_path = tmp_path / "data.csv"
    csv_path.write_text(
        "student,coffee_spent\nСтудент 1,100\nСтудент 2,200\n",
        encoding="utf-8",
    )

    records = load_records([csv_path])

    assert records == [
        Record(student="Студент 1", coffee_spent=100),
        Record(student="Студент 2", coffee_spent=200),
    ]


def test_load_records_raises_for_missing_file(tmp_path: Path) -> None:
    missing = tmp_path / "missing.csv"

    with pytest.raises(DataLoadError) as exc_info:
        load_records([missing])

    assert "Файл не найден" in str(exc_info.value)


def test_load_records_raises_for_missing_required_columns(tmp_path: Path) -> None:
    csv_path = tmp_path / "data.csv"
    csv_path.write_text(
        "student,other\nСтудент 1,100\n",
        encoding="utf-8",
    )

    with pytest.raises(DataLoadError) as exc_info:
        load_records([csv_path])

    msg = str(exc_info.value)
    assert "обязательные столбцы" in msg
    assert "coffee_spent" in msg


def test_load_records_skips_invalid_coffee_value(tmp_path: Path) -> None:
    csv_path = tmp_path / "data.csv"
    csv_path.write_text(
        "student,coffee_spent\nСтудент 1,not_a_number\nСтудент 2,200\n",
        encoding="utf-8",
    )

    records = load_records([csv_path])
    assert records == [
        Record(student="Студент 2", coffee_spent=200),
    ]
