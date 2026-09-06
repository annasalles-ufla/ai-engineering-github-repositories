from pathlib import Path
from core.analysis import RepositoryAnalysis
from core.classification import RelativeVisibilityClassifier
from core.loader import CsvRepositoryLoader
from core.report import TextReportBuilder

BASE_PATH = Path("assets/ai_engineering_ecosystem_intelligence.csv")
REPORT_PATH = Path("relatorio_analise.txt")
WIDTH = 72

def banner(title):
    print("\n" + "═" * WIDTH)
    print(title.center(WIDTH))
    print("═" * WIDTH)

def prompt(label):
    return input(f"  › {label}").strip()

def show_repositories(repositories, title):
    print(f"\n  {title} — {len(repositories)} resultado(s), exibindo até 10")
    print("  " + "─" * 66)
    for repo in repositories[:10]: print(f"  • {repo.full_name:<38} estrelas: {repo.stars:>7} | forks: {repo.forks:>6} | {repo.language}")

def main():
    repositories, invalid, missing = CsvRepositoryLoader().load(BASE_PATH)
    analysis, stats = RepositoryAnalysis(repositories), RepositoryAnalysis(repositories).statistics()
    classifier = RelativeVisibilityClassifier(stats["stars"]["mean"],stats["stars"]["mean"]*3,stats["forks"]["mean"],stats["forks"]["mean"]*3)
    while True:
        banner("TRABALHO FINAL — ANÁLISE DO ECOSSISTEMA DE IA")
        print("  [1] Estatísticas                [2] Busca textual")
        print("  [3] Filtrar por linguagem       [4] Ranking numérico")
        print("  [5] Gerar relatório             [0] Sair")
        print("─" * WIDTH)
        choice = prompt("Escolha uma opção: ")
        if choice == "1":
            print(f"\n  Válidos: {len(repositories):>8} | Inválidos: {len(invalid):>8}")
            print("  " + "─" * 66)
            for metric, values in stats.items(): print(f"  {metric:<13} média: {values['mean']:>10.2f} | mínimo: {values['min']:>8} | máximo: {values['max']:>8}")
        elif choice == "2": show_repositories(analysis.search(prompt("Texto: "),prompt("Campo (full_name/owner/repo_name/description): ") or "full_name"),"Busca")
        elif choice == "3": show_repositories(analysis.filter(language=prompt("Linguagem: ")),"Filtro")
        elif choice == "4": show_repositories(analysis.ranking(prompt("Métrica (stars/forks/open_issues/size_kb): ") or "stars"),"Ranking")
        elif choice == "5":
            TextReportBuilder().save(REPORT_PATH,analysis=analysis,invalid=invalid,missing=missing,classifier=classifier)
            print(f"Relatório salvo em {REPORT_PATH.resolve()}")
        elif choice == "0": break
        else: print("Opção inválida.")

if __name__ == "__main__": main()
