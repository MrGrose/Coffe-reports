from collections.abc import Iterable

from tabulate import tabulate


def print_table(headers: list[str], rows: Iterable[Iterable[object]]) -> None:
    table = tabulate(list(rows), headers=headers, tablefmt="github")
    print(table)
