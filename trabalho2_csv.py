"""Trabalho Prático 2 — processamento procedural do CSV completo."""
import csv
from collections import Counter
from pathlib import Path

BASE_PATH = Path("assets/ai_engineering_ecosystem_intelligence.csv")
REPORT_PATH = Path("relatorio_trabalho2.txt")
REQUIRED = ("full_name", "stars", "forks", "open_issues")
WIDTH = 72


def banner(title):
    print("\n" + "═" * WIDTH)
    print(title.center(WIDTH))
    print("═" * WIDTH)


def prompt(label):
    return input(f"  › {label}").strip()


def load_records(path):
    valid, invalid, missing = [], [], Counter()
    with path.open(encoding="utf-8-sig", newline="") as file:
        reader = csv.DictReader(file)
        absent = set(REQUIRED) - set(reader.fieldnames or [])
        if absent: raise ValueError(f"Cabeçalho sem campos obrigatórios: {', '.join(sorted(absent))}")
        for line, row in enumerate(reader, 2):
            for field, value in row.items():
                if not (value or "").strip(): missing[field] += 1
            try:
                for field in REQUIRED[1:]:
                    row[field] = int(row[field])
                    if row[field] < 0: raise ValueError(f"{field} negativo")
                if not row["full_name"].strip(): raise ValueError("full_name ausente")
                row["size_kb"] = int(row["size_kb"]) if (row.get("size_kb") or "").strip() else None
                if row["size_kb"] is not None and row["size_kb"] < 0: raise ValueError("size_kb negativo")
                valid.append(row)
            except (ValueError, TypeError) as error: invalid.append((line, str(error)))
    return valid, invalid, missing


def selection_sort(records, metric):
    """Ordenação por seleção decrescente, O(n²), implementada para a etapa 2."""
    ordered = records[:]
    for start in range(len(ordered) - 1):
        highest = start
        for index in range(start + 1, len(ordered)):
            if (ordered[index].get(metric) or 0) > (ordered[highest].get(metric) or 0): highest = index
        ordered[start], ordered[highest] = ordered[highest], ordered[start]
    return ordered


def statistics(records):
    if not records: return {}
    return {field: (sum(r[field] for r in records) / len(records), min(r[field] for r in records), max(r[field] for r in records)) for field in ("stars", "forks", "open_issues")}


def filter_records(records, field, value):
    if field in {"stars", "forks", "open_issues"}:
        low, high = map(int, value.split(":"))
        return [r for r in records if low <= r[field] <= high]
    return [r for r in records if (r.get(field) or "").casefold() == value.casefold()]


def show(records):
    print(f"\n  {len(records)} resultado(s); exibindo até 10")
    print("  " + "─" * 66)
    for row in records[:10]: print(f"  • {row['full_name']:<38} estrelas: {row['stars']:>7} | forks: {row['forks']:>6}")


def write_report(records, invalid, missing):
    stats = statistics(records)
    lines = ["RELATÓRIO — TRABALHO PRÁTICO 2", "Anna Waleska de Freitas Salles | RA 202621078", f"Lidos: {len(records)+len(invalid)} | Válidos: {len(records)} | Inválidos: {len(invalid)}", ""]
    lines += [f"{field}: média={values[0]:.2f}; mínimo={values[1]}; máximo={values[2]}" for field, values in stats.items()]
    lines += ["", "Por linguagem:"] + [f"{name}: {count}" for name,count in Counter(r.get("language") or "Não informado" for r in records).most_common(10)]
    lines += ["", "Dados ausentes:"] + [f"{name}: {count}" for name,count in missing.most_common(10)]
    REPORT_PATH.write_text("\n".join(lines)+"\n", encoding="utf-8")
    print(f"Relatório salvo em {REPORT_PATH.resolve()}")


def main():
    records, invalid, missing = load_records(BASE_PATH)
    while True:
        banner("TRABALHO PRÁTICO 2 — PROCESSAMENTO DO CSV")
        print("  [1] Resumo da base              [2] Buscar texto")
        print("  [3] Filtrar registros           [4] Ordenar e exibir ranking")
        print("  [5] Gerar relatório             [0] Sair")
        print("─" * WIDTH)
        option = prompt("Escolha uma opção: ")
        if option == "1":
            print(f"\n  Lidos: {len(records)+len(invalid):>8} | Válidos: {len(records):>8} | Inválidos: {len(invalid):>8}")
            print("  " + "─" * 66)
            for field, values in statistics(records).items(): print(f"  {field:<13} média: {values[0]:>10.2f} | mínimo: {values[1]:>8} | máximo: {values[2]:>8}")
        elif option == "2":
            field = prompt("Campo (full_name/owner/repo_name/description): ")
            term = prompt("Texto: ").casefold()
            show([r for r in records if term in (r.get(field) or "").casefold()])
        elif option == "3":
            field = prompt("Campo (language/license/license_family/stars/forks/open_issues): ")
            try: show(filter_records(records, field, prompt("Valor (faixa: mínimo:máximo): ")))
            except (ValueError, KeyError): print("Filtro ou faixa inválida.")
        elif option == "4":
            metric = prompt("Métrica (stars/forks/open_issues/size_kb): ")
            if metric in {"stars", "forks", "open_issues", "size_kb"}: show(selection_sort(records, metric))
            else: print("Métrica inválida.")
        elif option == "5": write_report(records, invalid, missing)
        elif option == "0": break
        else: print("Opção inválida.")


if __name__ == "__main__": main()
