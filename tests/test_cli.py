from pathlib import Path

from main import main


def test_cli_successful_run(tmp_path: Path, capsys) -> None:
    csv_path = tmp_path / "data.csv"
    csv_path.write_text(
        "student,coffee_spent\nСтудент 1,100\nСтудент 1,300\n",
        encoding="utf-8",
    )

    code = main(["--files", str(csv_path), "--report", "median-coffee"])
    captured = capsys.readouterr()

    assert code == 0
    assert "Студент 1" in captured.out
    assert "200" in captured.out


def test_cli_unknown_report(tmp_path: Path, capsys) -> None:
    csv_path = tmp_path / "data.csv"
    csv_path.write_text(
        "student,coffee_spent\nСтудент 1,100\n",
        encoding="utf-8",
    )

    code = main(["--files", str(csv_path), "--report", "unknown"])
    captured = capsys.readouterr()

    assert code == 1
    assert captured.out == ""
