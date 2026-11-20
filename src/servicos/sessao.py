
import time


class SessaoTreinamento:
    """Gerencia e cronometra uma sessao de treinamento."""

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
        self._tempo_total = (
            time.perf_counter() - self._inicio
        )

        print(
            f"[SESSAO] Tempo total: "
            f"{self._tempo_total:.2f} segundos"
        )

        if tipo_erro is not None:
            print(f"[SESSAO] Erro: {valor_erro}")
        else:
            print("[SESSAO] Finalizada com sucesso!")

        return False

    @property
    def tempo_total(self):
        return self._tempo_total
