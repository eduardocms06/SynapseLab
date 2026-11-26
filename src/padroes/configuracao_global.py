"""Configuracoes compartilhadas do framework usando o padrao Singleton."""
import threading
from pathlib import Path


class ConfiguracaoGlobal:
    """Mantem uma unica instancia e protege os parametros com Lock."""

    __instancia = None
    __trava_criacao = threading.Lock()

    def __new__(cls):
        with cls.__trava_criacao:
            if cls.__instancia is None:
                instancia = super().__new__(cls)
                instancia.__trava_dados = threading.Lock()
                instancia.__valores = {
                    "seed": 42,
                    "max_workers": 4,
                    "nivel_log": "INFO",
                    "diretorio_saida": "resultados",
                }
                cls.__instancia = instancia
            return cls.__instancia

    def configurar(self, *, seed=None, max_workers=None, nivel_log=None,
                   diretorio_saida=None):
        """Altera os parametros informados, mantendo os demais inalterados."""
        mudancas = {}
        if seed is not None:
            if type(seed) is not int:
                raise ValueError("seed deve ser um numero inteiro.")
            mudancas["seed"] = seed
        if max_workers is not None:
            if type(max_workers) is not int or max_workers < 1:
                raise ValueError("max_workers deve ser um inteiro positivo.")
            mudancas["max_workers"] = max_workers
        if nivel_log is not None:
            if not isinstance(nivel_log, str) or nivel_log.upper() not in (
                "DEBUG", "INFO", "WARNING", "ERROR", "SILENCIOSO"
            ):
                raise ValueError("nivel_log invalido.")
            mudancas["nivel_log"] = nivel_log.upper()
        if diretorio_saida is not None:
            if not str(diretorio_saida).strip():
                raise ValueError("diretorio_saida nao pode ser vazio.")
            mudancas["diretorio_saida"] = str(Path(diretorio_saida))
        with self.__trava_dados:
            self.__valores.update(mudancas)

    @property
    def seed(self):
        with self.__trava_dados:
            return self.__valores["seed"]

    @property
    def max_workers(self):
        with self.__trava_dados:
            return self.__valores["max_workers"]

    @property
    def nivel_log(self):
        with self.__trava_dados:
            return self.__valores["nivel_log"]

    @property
    def diretorio_saida(self):
        with self.__trava_dados:
            return self.__valores["diretorio_saida"]

    def obter_configuracao(self):
        """Devolve uma copia para evitar alteracoes externas sem sincronizacao."""
        with self.__trava_dados:
            return self.__valores.copy()

    def restaurar_padrao(self):
        """Restaura os valores iniciais, util para testes e novos experimentos."""
        with self.__trava_dados:
            self.__valores.update({
                "seed": 42,
                "max_workers": 4,
                "nivel_log": "INFO",
                "diretorio_saida": "resultados",
            })
