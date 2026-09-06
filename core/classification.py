from abc import ABC, abstractmethod
from .domain import NOT_INFORMED, Repository

class RepositoryClassifier(ABC):
    """Contrato para regras intercambiáveis de classificação (Strategy)."""
    @abstractmethod

    def classify(self, repository: Repository) -> str: raise NotImplementedError

class RelativeVisibilityClassifier(RepositoryClassifier):
    """Regra didática: estrelas e forks altos pontuam; licença declarada soma um ponto; muitos problemas relativos retiram um."""

    def __init__(self, star_medium: float, star_high: float, fork_medium: float, fork_high: float) -> None:
        self.star_medium, self.star_high = star_medium, star_high
        self.fork_medium, self.fork_high = fork_medium, fork_high

    def classify(self, repository: Repository) -> str:
        points = (2 if repository.stars >= self.star_high else 1 if repository.stars >= self.star_medium else 0)
        points += 2 if repository.forks >= self.fork_high else 1 if repository.forks >= self.fork_medium else 0
        points += repository.license != NOT_INFORMED
        if repository.stars and repository.open_issues / repository.stars > .20: points -= 1
        return "Alta visibilidade relativa" if points >= 4 else "Visibilidade relativa intermediária" if points >= 2 else "Baixa visibilidade relativa"
