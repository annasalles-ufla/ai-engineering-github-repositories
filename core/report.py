from datetime import date
from pathlib import Path

class TextReportBuilder:
    """Gera relatório reprodutível em texto, sem modificar a base de origem."""

    def build(self, analysis, invalid, missing, classifier) -> str:
        stats = analysis.statistics()
        lines = ["RELATÓRIO DESCRITIVO — ECOSSISTEMA DE ENGENHARIA DE IA", f"Data: {date.today():%d/%m/%Y}", "Estudante: Anna Waleska de Freitas Salles | RA: 202621078", "", f"Registros lidos: {len(analysis.repositories)+len(invalid)}", f"Registros válidos: {len(analysis.repositories)}", f"Registros inválidos: {len(invalid)}", f"Licenças não declaradas: {analysis.undeclared_licenses()}", "", "Métricas dos registros válidos:"]

        for metric, values in stats.items(): lines.append(f"- {metric}: média {values['mean']:.2f}; mínimo {values['min']}; máximo {values['max']}")
        lines += ["", "Distribuição por linguagem:"] + [f"- {name}: {count}" for name,count in analysis.distribution("language").most_common(10)]
        lines += ["", "Distribuição por família de licença:"] + [f"- {name}: {count}" for name,count in analysis.distribution("license_family").most_common(10)]
        lines += ["", "Ranking por estrelas (10 primeiros):"] + [f"- {repo.full_name}: {repo.stars}" for repo in analysis.ranking("stars", 10)]
        lines += ["", "Ranking por forks (10 primeiros):"] + [f"- {repo.full_name}: {repo.forks}" for repo in analysis.ranking("forks", 10)]
        lines += ["", "Dados ausentes por campo (10 maiores):"] + [f"- {field}: {count}" for field,count in missing.most_common(10)]
        lines += ["", "Classificação didática de visibilidade relativa:"] + [f"- {name}: {count}" for name,count in analysis.classify(classifier).items()]
        lines += ["", "Nota metodológica: os resultados descrevem somente esta base. Estrelas, forks, problemas e a classificação didática não são medidas definitivas de qualidade, segurança, maturidade ou adequação profissional."]
        return "\n".join(lines) + "\n"

    def save(self, path: Path, **kwargs) -> None: path.write_text(self.build(**kwargs), encoding="utf-8")
