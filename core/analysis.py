from collections import Counter
from statistics import mean
from typing import Iterable, Optional
from .classification import RepositoryClassifier
from .domain import NOT_INFORMED, Repository

class RepositoryAnalysis:
    """Serviço de consultas e estatísticas; não altera os registros carregados."""
    def __init__(self, repositories: Iterable[Repository]) -> None: self.repositories = tuple(repositories)

    def filter(self, *, language: Optional[str]=None, license_family: Optional[str]=None, star_range=None, fork_range=None, issue_range=None, category=None, maintenance_status=None):
        def matches(r): return ((not language or r.language.casefold()==language.casefold()) and (not license_family or r.license_family.casefold()==license_family.casefold()) and (not star_range or star_range[0]<=r.stars<=star_range[1]) and (not fork_range or fork_range[0]<=r.forks<=fork_range[1]) and (not issue_range or issue_range[0]<=r.open_issues<=issue_range[1]) and (not category or r.ai_category.casefold()==category.casefold()) and (not maintenance_status or r.maintenance_status.casefold()==maintenance_status.casefold()))
        return [r for r in self.repositories if matches(r)]

    def search(self, term: str, field="full_name", limit=20):
        if field not in {"full_name","owner","repo_name","description"}: raise ValueError("Campo de busca inválido")
        return [r for r in self.repositories if term.casefold().strip() in getattr(r,field).casefold()][:limit]

    def ranking(self, metric="stars", limit=10):
        if metric not in {"stars","forks","open_issues","size_kb"}: raise ValueError("Métrica de ordenação inválida")
        return sorted(self.repositories,key=lambda r:getattr(r,metric) or 0,reverse=True)[:limit]

    def statistics(self):
        return {m:{"mean":mean(getattr(r,m) for r in self.repositories),"min":min(getattr(r,m) for r in self.repositories),"max":max(getattr(r,m) for r in self.repositories)} for m in ("stars","forks","open_issues")} if self.repositories else {}

    def distribution(self, field):
        if field not in {"language","license_family","ai_category","maintenance_status"}: raise ValueError("Campo de distribuição inválido")
        return Counter(getattr(r,field) for r in self.repositories)

    def mean_by(self, group_field, metric="stars", minimum_group_size=5):
        groups = {}
        for r in self.repositories: groups.setdefault(getattr(r,group_field),[]).append(getattr(r,metric))
        return {key:mean(values) for key,values in groups.items() if len(values)>=minimum_group_size}

    def classify(self, classifier: RepositoryClassifier): return Counter(classifier.classify(r) for r in self.repositories)

    def undeclared_licenses(self): return sum(r.license == NOT_INFORMED for r in self.repositories)
