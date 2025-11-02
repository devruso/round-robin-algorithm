import argparse
import json
import os
import csv
from src.round_robin import simulate_from_dicts


def parse_input_file(path: str):
    ext = os.path.splitext(path)[1].lower()
    if ext == '.json':
        with open(path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        return data
    elif ext == '.csv':
        processos = []
        with open(path, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                processos.append({
                    'nome': row.get('nome') or row.get('Nome') or row.get('NAME'),
                    'chegada': int(row.get('chegada') or row.get('Chegada') or row.get('arrival')),
                    'execucao': int(row.get('execucao') or row.get('Execucao') or row.get('burst')),
                })
        return processos
    else:
        raise ValueError('Formato de arquivo não suportado. Use .json ou .csv')


def print_gantt(timeline: list):
    if not timeline:
        print('Gantt: (vazio)')
        return
    # imprime índices
    indices = ' '.join(str(i) for i in range(len(timeline)))
    procs = ' '.join(timeline)
    print('\nGantt chart (cada unidade de tempo):')
    print(indices)
    print(procs)


def main():
    parser = argparse.ArgumentParser(description='Simulador Round Robin (quantum=2 por padrão)')
    parser.add_argument('--input', '-i', help='arquivo JSON ou CSV com processos (campo nome, chegada, execucao)')
    parser.add_argument('--quantum', '-q', type=int, default=2, help='quantum (padrão 2)')
    parser.add_argument('--gantt', action='store_true', help='imprimir Gantt chart textual por unidade de tempo')
    args = parser.parse_args()

    if args.input:
        processos = parse_input_file(args.input)
    else:
        processos = [
            {"nome": "P1", "chegada": 0, "execucao": 5},
            {"nome": "P2", "chegada": 1, "execucao": 3},
            {"nome": "P3", "chegada": 2, "execucao": 6},
        ]

    ret = simulate_from_dicts(processos, quantum=args.quantum, return_timeline=True)
    if len(ret) == 5:
        ordem, respostas, media, processos_result, timeline = ret
    else:
        ordem, respostas, media, processos_result = ret
        timeline = []

    print("Simulação Round Robin (quantum={})\n".format(args.quantum))
    print("Ordem de execução:")
    print(' -> '.join(ordem))

    print("\nTempos por processo:")
    for p in processos_result:
        print(f"{p.nome}: chegada={p.chegada}, inicio={p.inicio}, termino={p.termino}, resposta={respostas[p.nome]}")

    print(f"\nTempo médio de resposta: {media:.2f}")


    if args.gantt:
        print_gantt(timeline)


if __name__ == '__main__':
    main()
