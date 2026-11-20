import threading
from copy import deepcopy


class HistoricoExecucao:
    """Guarda os resultados compartilhados entre as threads."""

    def __init__(self):
        self.__registros = []
        self.__trava = threading.Lock()

    def registrar_resultado(self, resultado):
        with self.__trava:
            self.__registros.append(deepcopy(resultado))

    def obter_resultados(self):
        with self.__trava:
            return deepcopy(self.__registros)

    def quantidade_resultados(self):
        with self.__trava:
            return len(self.__registros)


def executar_treinamentos(valores_k, tarefa_treinamento, historico=None):
    """Inicia todas as threads e espera a conclusao de cada uma."""
    if historico is None:
        historico = HistoricoExecucao()

    erros = []
    trava_erros = threading.Lock()

    def executar_tarefa(k):
        try:
            resultado = tarefa_treinamento(k)
            historico.registrar_resultado(resultado)
        except Exception as erro:
            with trava_erros:
                erros.append(erro)

    threads = []
    for k in valores_k:
        thread = threading.Thread(target=executar_tarefa, args=(k,))
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

    if erros:
        raise RuntimeError("Um ou mais treinamentos falharam.") from erros[0]

    return historico
