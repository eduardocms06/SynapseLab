
import threading


class HistoricoExecucao:
    """Armazena resultados de forma segura entre threads."""

    def __init__(self):
        self.__registros = []
        self.__trava = threading.Lock()

    def registrar_resultado(self, resultado):
        """Adiciona um resultado ao historico."""
        with self.__trava:
            self.__registros.append(resultado)

    def obter_resultados(self):
        """Retorna uma copia dos resultados armazenados."""
        with self.__trava:
            return self.__registros.copy()

    def quantidade_resultados(self):
        """Retorna a quantidade de registros."""
        with self.__trava:
            return len(self.__registros)

def executar_treinamentos(valores_k, tarefa_treinamento, historico=None):
    """Executa varios treinamentos usando threads."""

    if historico is None:
        historico = HistoricoExecucao()

    threads = []
    erros = []
    trava_erros = threading.Lock()

    def executar_tarefa(k):
        try:
            resultado = tarefa_treinamento(k)
            historico.registrar_resultado(resultado)

        except Exception as erro:
            with trava_erros:
                erros.append(erro)

    # Criar e iniciar todas as threads
    for k in valores_k:
        thread = threading.Thread(
            target=executar_tarefa,
            args=(k,)
        )

        threads.append(thread)
        thread.start()

    # Aguardar todas as threads terminarem
    for thread in threads:
        thread.join()

    if erros:
        raise RuntimeError(
            "Um ou mais treinamentos falharam."
        ) from erros[0]

    return historico
