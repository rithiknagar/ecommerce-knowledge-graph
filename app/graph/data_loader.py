import csv
from pathlib import Path
from typing import Any


class CSVDataLoader:
    def __init__(self, data_directory: Path) -> None:
        self.data_directory = data_directory

    def load(self, filename: str) -> list[dict[str, Any]]:
        file_path = self.data_directory / filename

        with file_path.open(
            mode="r",
            encoding="utf-8",
            newline="",
        ) as file:
            reader = csv.DictReader(file)

            return list(reader)