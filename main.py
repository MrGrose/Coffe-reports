import logging
import sys

from src.loader.data_loader import DataLoadError, load_records
from src.reports.base import ReportError
from src.utils.arg_parser import build_parser
from src.utils.registry import get_report
from src.utils.table_printer import print_table

logger = logging.getLogger(__name__)


def main(argv: list[str] | None = None) -> int:

    logging.basicConfig(
        level=logging.ERROR,
        stream=sys.stderr,
        format="%(message)s",
    )
    parser = build_parser()
    args = parser.parse_args(argv)
    try:
        records = load_records(args.files)
        report = get_report(args.report)
        result = report.generate(records)
        print_table(result.headers, result.rows)

    except DataLoadError as exc:
        logger.error("Ошибка загрузки данных: %s", exc)
        return 1
    except ReportError as exc:
        logger.error("Ошибка формирования отчёта: %s", exc)
        return 1
    except Exception as exc:
        logger.exception("Неизвестная ошибка: %s", exc)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
