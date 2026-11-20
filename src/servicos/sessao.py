import time


class SessaoTreinamento:
    """Mede o tempo de um treinamento com o comando with."""

    def __init__(self, nome="Treinamento"):
        self.nome = nome
        self._inicio = None
        self._tempo_total = None

    def __enter__(self):
        self._inicio = time.perf_counter()
        self._tempo_total = None
        print(f"[SESSAO] Iniciando: {self.nome}")
        return self

    def __exit__(self, tipo_erro, valor_erro, traceback):
        self._tempo_total = time.perf_counter() - self._inicio
        print(f"[SESSAO] Tempo total: {self._tempo_total:.2f} segundos")

        if tipo_erro is not None:
            print(f"[SESSAO] Erro: {valor_erro}")
        else:
            print("[SESSAO] Finalizada com sucesso!")

        return False  # Nao esconde erros do treinamento

    @property
    def tempo_total(self):
        return self._tempo_total
