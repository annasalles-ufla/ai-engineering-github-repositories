"""Trabalho Prático 1 — análise procedural de poucos repositórios.

Não lê arquivos: os dados são cadastrados durante a execução.
"""

NOT_INFORMED = "Não informado"
WIDTH = 72


def banner(title):
    print("\n" + "═" * WIDTH)
    print(title.center(WIDTH))
    print("═" * WIDTH)


def prompt(label):
    return input(f"  › {label}").strip()


def read_non_negative_integer(label):
    while True:
        try:
            value = int(prompt(label))
            if value >= 0:
                return value
        except ValueError:
            pass
        print("Informe um número inteiro não negativo.")


def read_text(label, required=False):
    while True:
        value = prompt(label)
        if value or not required:
            return value or NOT_INFORMED
        print("Este campo é obrigatório.")


def create_repository():
    full_name = read_text("Nome completo (owner/repositório): ", required=True)
    owner = read_text("Proprietário: ")
    repo_name = read_text("Nome do repositório: ")
    return {
        "full_name": full_name, "owner": owner, "repo_name": repo_name,
        "language": read_text("Linguagem: "), "stars": read_non_negative_integer("Estrelas: "),
        "forks": read_non_negative_integer("Forks: "), "open_issues": read_non_negative_integer("Problemas abertos: "),
        "license": read_text("Licença: "),
    }


def classify(repository):
    """Regra didática: nunca representa qualidade, segurança ou maturidade."""
    points = 0
    if repository["stars"] >= 100: points += 2
    elif repository["stars"] >= 20: points += 1
    if repository["forks"] >= 20: points += 2
    elif repository["forks"] >= 5: points += 1
    if repository["license"] != NOT_INFORMED: points += 1
    if repository["stars"] and repository["open_issues"] / repository["stars"] > .20: points -= 1
    return "Alta visibilidade relativa" if points >= 4 else "Visibilidade relativa intermediária" if points >= 2 else "Baixa visibilidade relativa"


def show_statistics(repositories):
    if not repositories:
        print("\n  Nenhum registro cadastrado ainda.")
        return
    for metric in ("stars", "forks", "open_issues"):
        values = [repo[metric] for repo in repositories]
        print(f"  {metric:<13} média: {sum(values)/len(values):>10.2f} | mínimo: {min(values):>8} | máximo: {max(values):>8}")
    for field in ("language", "license"):
        counts = {}
        for repo in repositories: counts[repo[field]] = counts.get(repo[field], 0) + 1
        print(f"  Distribuição por {field}: {counts}")


def show_results(repositories):
    if not repositories:
        print("\n  Nenhum resultado encontrado.")
        return
    print(f"\n  {len(repositories)} resultado(s)")
    print("  " + "─" * 66)
    for repo in repositories:
        print(f"  • {repo['full_name']:<35} estrelas: {repo['stars']:>6} | {classify(repo)}")


def main():
    repositories = []
    while True:
        banner("TRABALHO PRÁTICO 1 — ANÁLISE PROCEDURAL")
        print("  [1] Cadastrar repositórios      [2] Estatísticas")
        print("  [3] Filtrar registros           [4] Consultar por full_name")
        print("  [5] Classificar registros       [0] Sair")
        print("─" * WIDTH)
        option = prompt("Escolha uma opção: ")
        if option == "1":
            quantity = read_non_negative_integer("Quantidade de repositórios: ")
            for _ in range(quantity): repositories.append(create_repository())
        elif option == "2": show_statistics(repositories)
        elif option == "3":
            field = prompt("Filtro (language/license/stars): ")
            if field == "stars":
                low, high = read_non_negative_integer("Mínimo: "), read_non_negative_integer("Máximo: ")
                show_results([r for r in repositories if low <= r["stars"] <= high])
            elif field in {"language", "license"}:
                value = prompt("Valor: ").casefold()
                show_results([r for r in repositories if r[field].casefold() == value])
            else: print("Filtro inválido.")
        elif option == "4":
            name = prompt("full_name: ").casefold()
            show_results([r for r in repositories if r["full_name"].casefold() == name])
        elif option == "5":
            show_results(repositories)
        elif option == "0": break
        else: print("Opção inválida.")


if __name__ == "__main__": main()
