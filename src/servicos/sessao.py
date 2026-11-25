"""Cronometra uma sessao e registra se a execucao terminou com sucesso."""
import time


class SessaoTreinamento:
    """Registra o tempo e se a execucao terminou sem excecao."""

    def __init__(self, identificador="Treinamento"):
        self.__identificador = identificador
        self.__tempo_inicio = None
        self.__tempo_total = None
        self.__sucesso = False

    @property
    def tempo_total(self):
        return self.__tempo_total

    @property
    def sucesso(self):
        return self.__sucesso

    def __enter__(self):
        self.__tempo_inicio = time.perf_counter()
        self.__tempo_total = None
        self.__sucesso = False
        print(f"[SESSAO] Iniciando: {self.__identificador}")
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.__tempo_total = time.perf_counter() - self.__tempo_inicio
        self.__sucesso = exc_type is None
        print(f"[SESSAO] Tempo total: {self.__tempo_total:.2f} segundos")
        if self.__sucesso:
            print("[SESSAO] Finalizada com sucesso!")
        else:
            print(f"[SESSAO] Erro: {exc_val}")
        return False  # Nunca esconde a excecao
