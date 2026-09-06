import csv
from abc import ABC, abstractmethod
from collections import Counter
from pathlib import Path
from typing import Mapping, Optional
from .domain import InvalidRecord, NOT_INFORMED, Repository

REQUIRED_COLUMNS = {"full_name", "owner", "repo_name", "language", "stars", "forks", "open_issues", "license", "license_family"}

class RepositoryLoader(ABC):
    @abstractmethod
    def load(self, path: Path): raise NotImplementedError

class CsvRepositoryLoader(RepositoryLoader):
    """Leitor CSV: valida métricas essenciais e mantém o arquivo original intacto."""

    @staticmethod
    def _text(row: Mapping[str, str], field: str) -> str: return (row.get(field) or "").strip() or NOT_INFORMED

    @staticmethod
    def _integer(row: Mapping[str, str], field: str, required: bool = True) -> Optional[int]:
        value = (row.get(field) or "").strip()
        if not value:
            if required: raise ValueError(f"{field} ausente")
            return None
        try: number = int(value)
        except ValueError as error: raise ValueError(f"{field} não é numérico") from error
        if number < 0: raise ValueError(f"{field} é negativo")
        return number

    def load(self, path: Path):
        repositories, invalid, missing = [], [], Counter()
        with path.open("r", encoding="utf-8-sig", newline="") as csv_file:
            reader = csv.DictReader(csv_file)
            absent = REQUIRED_COLUMNS - set(reader.fieldnames or [])
            if absent: raise ValueError(f"Colunas obrigatórias ausentes: {', '.join(sorted(absent))}")
            for line_number, row in enumerate(reader, start=2):
                for field, value in row.items():
                    if not (value or "").strip(): missing[field] += 1
                try:
                    full_name = self._text(row, "full_name")
                    if full_name == NOT_INFORMED: raise ValueError("full_name ausente")
                    repositories.append(Repository(full_name, self._text(row,"owner"), self._text(row,"repo_name"), self._text(row,"description"), self._text(row,"html_url"), self._text(row,"language"), self._integer(row,"stars"), self._integer(row,"forks"), self._integer(row,"open_issues"), self._integer(row,"size_kb",False), self._text(row,"license"), self._text(row,"license_family"), self._text(row,"ai_category"), self._text(row,"maintenance_status")))
                except ValueError as error: invalid.append(InvalidRecord(line_number, str(error)))
        return repositories, invalid, missing
