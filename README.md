# Simulador Round Robin (Python)

Este projeto implementa uma simulação do algoritmo de escalonamento Round Robin com quantum = 2.


Arquivos principais
- `src/round_robin.py`: implementação da simulação (classe `RoundRobinScheduler`) e exemplo padrão.
- `tests/test_round_robin.py`: teste unitário que valida o exemplo do enunciado.

- `app.py`: entrada (main) que utiliza a lista de dicionários sugerida na "dica" e imprime os resultados da simulação.

Como executar

1. Para rodar a simulação de exemplo (arquivo `app.py` que usa o formato da dica):

```bash
python app.py
```
ou adicione --grant para ver mais detalhes sobre a execução do algoritmo

```bash
python app.py --grant
```

Opções CLI

```bash
# rodar exemplo padrão
python app.py --bash


# mudar o quantum
python app.py --quantum 3
```

2. Para executar os testes (usa unittest, sem dependências externas):

```bash
python -m unittest discover -v
```

O exemplo padrão usa os processos:

```
P1: chegada=0, execucao=5
P2: chegada=1, execucao=3
P3: chegada=2, execucao=6
```

Resultados esperados (do exercício):

- Ordem de execução: P1 → P2 → P3 → P1 → P2 → P3 → P1 → P3
- Tempos de resposta: P1=0, P2=1, P3=2
- Tempo médio de resposta: 1.0

Formato de entrada

O `app.py` espera uma lista de dicionários com as chaves: `nome`, `chegada`, `execucao`.

Exemplo:

```python
processos = [
	{"nome": "P1", "chegada": 0, "execucao": 5},
	{"nome": "P2", "chegada": 1, "execucao": 3},
	{"nome": "P3", "chegada": 2, "execucao": 6},
]
```

Formato CSV

O CSV deve ter cabeçalho com pelo menos as colunas `nome`, `chegada`, `execucao` (case-insensitive). Exemplo:

```
nome,chegada,execucao
P1,0,5
P2,1,3
P3,2,6
```

