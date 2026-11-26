from abc import ABC, abstractmethod

class IEstrategiaDistancia(ABC):
    @abstractmethod
    def calcular(self, p1: list[float], p2: list[float]) -> float: ...  