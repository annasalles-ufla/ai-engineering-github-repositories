# Análise do ecossistema de engenharia de IA

Projeto universitário de **Anna Waleska de Freitas Salles** — **RA 202621078**. Sistema em Python orientado a objetos para análise descritiva de `assets/ai_engineering_ecosystem_intelligence.csv`.

## Problema que o projeto resolve

A base fornecida reúne mais de 30 mil repositórios públicos do GitHub relacionados à engenharia de inteligência artificial. Consultar esse volume de dados manualmente dificulta responder perguntas simples, por exemplo: quantos registros são válidos, quais linguagens aparecem com maior frequência, quais repositórios têm mais estrelas ou forks, e como filtrar projetos por licença, categoria ou faixa de métricas.

O projeto resolve esse problema ao ler a base CSV sem alterá-la, validar os dados e disponibilizar consultas e relatórios descritivos. Assim, os registros podem ser organizados e comparados dentro do conjunto fornecido, sem utilizar inteligência artificial, aprendizado de máquina, serviços externos ou análise preditiva.

## Como o sistema funciona

1. O programa lê `assets/ai_engineering_ecosystem_intelligence.csv`; cada linha representa um repositório e o cabeçalho define os campos disponíveis.
2. Durante a leitura, os campos `full_name`, `stars`, `forks` e `open_issues` são validados. Linhas com métricas ausentes, não numéricas ou negativas são registradas como inválidas. Campos textuais vazios recebem o rótulo `Não informado`; `size_kb` pode permanecer ausente.
3. Os registros válidos são mantidos em memória para permitir buscas por texto, filtros, contagens, médias, mínimos, máximos, distribuições e rankings.
4. O usuário escolhe as operações em um menu exibido no terminal. Listagens extensas mostram apenas os primeiros resultados, evitando saídas excessivas.
5. Quando solicitado, o sistema salva um relatório textual com os indicadores calculados, dados ausentes e uma observação metodológica.

As estrelas, forks, problemas abertos e a classificação do projeto são indicadores presentes no arquivo. Eles não devem ser interpretados como medidas definitivas de qualidade, segurança, maturidade ou adequação profissional de um repositório.

## Entregas separadas e execução

Requer Python 3.10+ e apenas a biblioteca padrão:

```powershell
# Trabalho 1: procedural e cadastro manual de poucos registros
python trabalho1_procedural.py

# Trabalho 2: procedural, leitura do CSV e ordenação por seleção
python trabalho2_csv.py

# Trabalho Final: sistema orientado a objetos
python main.py

# Testes automatizados dos três programas
python -m unittest discover -s tests -v
```

| Entrega | Arquivo | Escopo |
|---|---|---|
| Trabalho 1 | `trabalho1_procedural.py` | Cadastro manual, validação, cálculos, filtros, consulta e classificação procedural. |
| Trabalho 2 | `trabalho2_csv.py` | Leitura do CSV, validação, buscas, filtros, estatísticas, relatório e Selection Sort próprio. |
| Trabalho Final | `main.py` e `core/` | Arquitetura OO, entidades imutáveis, abstração, polimorfismo, Strategy, consultas e relatório. |

O Trabalho Final também disponibiliza filtros combináveis por família de licença, faixas de estrelas/forks/problemas, categoria e estado de manutenção.

### Regra de classificação didática

No Trabalho 1 e no Trabalho Final existe uma classificação de **visibilidade relativa**. Ela utiliza limites de estrelas e forks, a existência de licença declarada e uma penalização quando a proporção de problemas abertos é alta em relação às estrelas. No Trabalho Final, os limites são calculados a partir das médias da própria base e a regra é implementada pelo padrão Strategy. O resultado é determinístico e serve somente como exercício de programação e organização dos dados da base.

## Estrutura e decisões

- `trabalho1_procedural.py`: somente funções e dicionários; não lê arquivos.
- `trabalho2_csv.py`: somente funções e dicionários; inclui Selection Sort para demonstrar o algoritmo da disciplina.
- `core/domain.py`: entidades imutáveis da etapa final.
- `core/loader.py`: leitura e validação do CSV. `full_name`, `stars`, `forks` e `open_issues` são obrigatórios; métricas ausentes/negativas tornam a linha inválida. Texto vazio é normalizado para `Não informado` e `size_kb` pode ficar ausente.
- `core/analysis.py`: consultas, filtros, ordenação e estatísticas.
- `core/classification.py`: padrão Strategy, com regra determinística de visibilidade relativa. É didática e não mede qualidade, segurança ou maturidade.
- `core/report.py`: relatório textual.

Médias, mínimos, máximos e distribuições usam somente registros válidos. A busca na descrição é uma comparação convencional de strings, sem IA, modelos preditivos ou serviços externos.

## Complexidade

Leitura, filtros, busca e estatísticas: **O(n)**. Rankings: **O(n log n)**. Memória: **O(n)** para os registros válidos.
