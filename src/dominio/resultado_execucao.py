"""Representa a avaliacao de um modelo, incluindo metricas e duracao."""
from copy import deepcopy


class ResultadoExecucao:
    """Um resultado de avaliacao de um modelo."""

    def __init__(self, nome, acuracia, tempo, detalhes=None):
        if not isinstance(nome, str) or not nome:
            raise ValueError("Informe o nome do modelo.")
        if not 0 <= acuracia <= 1:
            raise ValueError("A acuracia precisa estar entre 0 e 1.")
        if tempo < 0:
            raise ValueError("O tempo nao pode ser negativo.")
        self.__nome_modelo = nome
        self.__acuracia = float(acuracia)
        self.__tempo_segundos = float(tempo)
        self.__metricas_detalhadas = deepcopy(detalhes or {})

    @property
    def nome_modelo(self):
        return self.__nome_modelo

    @property
    def acuracia(self):
        return self.__acuracia

    @property
    def tempo_segundos(self):
        return self.__tempo_segundos

    @property
    def metricas_detalhadas(self):
        return deepcopy(self.__metricas_detalhadas)

    def para_dict(self):
        return {
            "nome_modelo": self.nome_modelo,
            "acuracia": self.acuracia,
            "tempo_segundos": self.tempo_segundos,
            "metricas_detalhadas": self.metricas_detalhadas,
        }

    def __str__(self):
        return f"{self.nome_modelo}: {self.acuracia:.2%} ({self.tempo_segundos:.4f}s)"

    def __repr__(self):
        return (f"ResultadoExecucao(nome={self.nome_modelo!r}, "
                f"acuracia={self.acuracia!r}, tempo={self.tempo_segundos!r}, "
                f"detalhes={self.metricas_detalhadas!r})")

    def __eq__(self, other):
        if not isinstance(other, ResultadoExecucao):
            return NotImplemented
        return self.para_dict() == other.para_dict()

    def __lt__(self, other):
        if not isinstance(other, ResultadoExecucao):
            return NotImplemented
        return (self.acuracia, -self.tempo_segundos) < (other.acuracia, -other.tempo_segundos)
