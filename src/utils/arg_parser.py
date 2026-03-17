import argparse

from src.utils.registry import get_available_reports


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description=(
            "Формирование отчётов по данным о подготовке студентов к экзаменам."
        )
    )
    parser.add_argument(
        "--files",
        nargs="+",
        required=True,
        metavar="ПУТЬ_К_ФАЙЛУ",
        help="Пути к CSV-файлам с данными.",
    )
    parser.add_argument(
        "--report",
        required=True,
        metavar="ИМЯ_ОТЧЁТА",
        help=f"Название отчёта (доступные: {', '.join(get_available_reports())}).",
    )

    return parser
