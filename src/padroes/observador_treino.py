"""Interface e observadores de eventos de treinamento (padrao Observer)."""
from abc import ABC, abstractmethod
from copy import deepcopy
import threading

from src.padroes.configuracao_global import ConfiguracaoGlobal


class IObservadorTreino(ABC):
    """Contrato dos componentes que acompanham um Experimento."""

    @abstractmethod
    def atualizar(self, evento):
        """Recebe um evento com pelo menos a chave 'tipo'."""

    @property
    def parada_solicitada(self):
        """Por padrao, um observador nao interrompe o experimento."""
        return False


class LoggerTreino(IObservadorTreino):
    """Guarda os eventos e pode apresenta-los no terminal."""

    def __init__(self, exibir_console=True):
        self.__eventos = []
        self.__trava = threading.Lock()
        self.__exibir_console = exibir_console

    @property
    def eventos(self):
        with self.__trava:
            return deepcopy(self.__eventos)

    def atualizar(self, evento):
        tipo = evento.get("tipo", "evento")
        with self.__trava:
            self.__eventos.append(deepcopy(evento))
            nivel = ConfiguracaoGlobal().nivel_log
            if not self.__exibir_console or nivel == "SILENCIOSO":
                return
            if nivel in ("WARNING", "ERROR") and tipo != "erro_experimento":
                return
            if nivel == "INFO" and tipo == "inicio_etapa":
                return
            if tipo == "etapa_concluida":
                resultado = evento.get("resultado", {})
                nome = resultado.get("nome_modelo", resultado.get("modelo", "Modelo"))
                acuracia = resultado.get("acuracia")
                tempo = resultado.get("tempo_segundos")
                resumo = f"[TREINO] {nome} concluido"
                if evento.get("fold") is not None:
                    resumo += f" (fold {evento['fold']})"
                if acuracia is not None:
                    resumo += f" | acuracia: {acuracia:.2%}"
                if tempo is not None:
                    resumo += f" | tempo: {tempo:.4f}s"
                print(resumo)
            else:
                print(f"[TREINO] {tipo}: {evento.get('titulo', 'Experimento')}")


class MonitorParadaAntecipada(IObservadorTreino):
    """Solicita parar novos lotes ao atingir a meta ou ficar sem melhora."""

    def __init__(self, paciencia=3, melhoria_minima=0.0, acuracia_alvo=None):
        if type(paciencia) is not int or paciencia < 1:
            raise ValueError("paciencia deve ser um inteiro positivo.")
        if not 0 <= melhoria_minima <= 1:
            raise ValueError("melhoria_minima deve estar entre 0 e 1.")
        if acuracia_alvo is not None and not 0 <= acuracia_alvo <= 1:
            raise ValueError("acuracia_alvo deve estar entre 0 e 1.")
        self.__paciencia = paciencia
        self.__melhoria_minima = melhoria_minima
        self.__acuracia_alvo = acuracia_alvo
        self.__trava = threading.Lock()
        self.__parada = threading.Event()
        self.__melhor_acuracia = None
        self.__sem_melhoria = 0

    @property
    def parada_solicitada(self):
        return self.__parada.is_set()

    @property
    def melhor_acuracia(self):
        with self.__trava:
            return self.__melhor_acuracia

    def atualizar(self, evento):
        tipo = evento.get("tipo")
        if tipo == "inicio_experimento":
            with self.__trava:
                self.__melhor_acuracia = None
                self.__sem_melhoria = 0
                self.__parada.clear()
            return
        if tipo != "etapa_concluida":
            return
        resultado = evento.get("resultado", {})
        acuracia = resultado.get("acuracia")
        if acuracia is None:
            return
        with self.__trava:
            if self.__melhor_acuracia is None or acuracia > self.__melhor_acuracia + self.__melhoria_minima:
                self.__melhor_acuracia = acuracia
                self.__sem_melhoria = 0
            else:
                self.__sem_melhoria += 1
            if (self.__acuracia_alvo is not None and acuracia >= self.__acuracia_alvo) or (
                self.__sem_melhoria >= self.__paciencia
            ):
                self.__parada.set()
