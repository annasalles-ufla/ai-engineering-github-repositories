from __future__ import annotations
from dataclasses import dataclass
from typing import Optional

NOT_INFORMED = "Não informado"

@dataclass(frozen=True, slots=True)
class Repository:
    """Entidade imutável que representa um registro válido da base."""
    full_name: str; owner: str; repo_name: str; description: str; html_url: str; language: str
    stars: int; forks: int; open_issues: int; size_kb: Optional[int]; license: str; license_family: str
    ai_category: str = NOT_INFORMED
    maintenance_status: str = NOT_INFORMED

@dataclass(frozen=True, slots=True)
class InvalidRecord:
    line_number: int
    reason: str
