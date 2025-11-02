from dataclasses import dataclass, field
from typing import List, Optional, Tuple, Dict


@dataclass
class Process:
    nome: str
    chegada: int
    execucao: int
    inicio: Optional[int] = None
    termino: Optional[int] = None
    restante: int = field(init=False)
    """Representa um processo no simulador.

    Campos:
    - nome: identificador do processo
    - chegada: instante de chegada
    - execucao: tempo total de CPU necessário (burst)
    - inicio: instante em que foi escalado pela primeira vez
    - termino: instante em que terminou
    - restante: tempo de execução restante (inicialmente igual a execucao)
    """

    def __post_init__(self):
        self.restante = int(self.execucao)


class RoundRobinScheduler:
    def __init__(self, processos: List[Process], quantum: int = 2):
        # ordena por tempo de chegada para facilitar a enfileiração
        self.processos = sorted(processos, key=lambda p: p.chegada)
        self.quantum = quantum

    def simulate(self, return_timeline: bool = False) -> Tuple[List[str], Dict[str, int], float, List[Process]]:
        """Executa a simulação do algoritmo Round Robin.

        Se return_timeline for True, a função também retorna um registro por unidade de tempo
        (lista de nomes indicando qual processo executou em cada tick).

        Retorno (sem timeline): (ordem_execucao, respostas, media_resposta, processos)
        Retorno (com timeline): (ordem_execucao, respostas, media_resposta, processos, timeline)
        """

        tempo = 0
        fila: List[Process] = []
        ordem_execucao: List[str] = []
        timeline: List[str] = []
        chegada_idx = 0
        total_processos = len(self.processos)
        finalizados = 0

        def enfileirar_chegadas():
            nonlocal chegada_idx, tempo
            while chegada_idx < len(self.processos) and self.processos[chegada_idx].chegada <= tempo:
                fila.append(self.processos[chegada_idx])
                chegada_idx += 1

        enfileirar_chegadas()

        while finalizados < total_processos:
            if not fila:
                if chegada_idx < len(self.processos):
                    tempo = max(tempo, self.processos[chegada_idx].chegada)
                    enfileirar_chegadas()
                    continue
                else:
                    break

            proc = fila.pop(0)

            if proc.inicio is None:
                proc.inicio = tempo

            fatia = min(self.quantum, proc.restante)
            ordem_execucao.append(proc.nome)

            for _ in range(fatia):
                tempo += 1
                timeline.append(proc.nome)
                enfileirar_chegadas()

            proc.restante -= fatia

            if proc.restante == 0:
                proc.termino = tempo
                finalizados += 1
            else:
                fila.append(proc)

        respostas: Dict[str, int] = {}
        soma_resposta = 0
        for p in self.processos:
            if p.inicio is None:
                respostas[p.nome] = -1
            else:
                resp = p.inicio - p.chegada
                respostas[p.nome] = resp
                soma_resposta += resp

        media_resposta = soma_resposta / total_processos if total_processos else 0.0

        if return_timeline:
            return ordem_execucao, respostas, media_resposta, self.processos, timeline
        return ordem_execucao, respostas, media_resposta, self.processos


def default_example() -> List[Process]:
    dados = [
        {"nome": "P1", "chegada": 0, "execucao": 5},
        {"nome": "P2", "chegada": 1, "execucao": 3},
        {"nome": "P3", "chegada": 2, "execucao": 6},
    ]
    return [Process(**d) for d in dados]


def main():
    processos = default_example()
    scheduler = RoundRobinScheduler(processos, quantum=2)
    ordem, respostas, media, processos_result = scheduler.simulate()

    print("\nSimulação Round Robin (quantum=2)")
    print("Ordem de execução:")
    print(' -> '.join(ordem))

    print("\nTempos por processo:")
    for p in processos_result:
        print(f"{p.nome}: chegada={p.chegada}, inicio={p.inicio}, termino={p.termino}, resposta={respostas[p.nome]}")

    print(f"\nTempo médio de resposta: {media:.2f}")

    print("\nComparação com simuladores externos: forneça os valores do simulador LotusOregano para comparação.")


if __name__ == '__main__':
    main()


def simulate_from_dicts(processos_dicts, quantum: int = 2, return_timeline: bool = False):
    """
    Wrapper que aceita uma lista de dicionários no formato sugerido na dica:
    [{"nome": "P1", "chegada": 0, "execucao": 5}, ...]

    Retorna: ordem_execucao, respostas, media_resposta, lista_de_processos
    """
    processos = [Process(nome=d["nome"], chegada=d["chegada"], execucao=d["execucao"]) for d in processos_dicts]
    scheduler = RoundRobinScheduler(processos, quantum=quantum)
    return scheduler.simulate(return_timeline)
