"""Define as operacoes de salvar e carregar que as persistencias implementam."""
from abc import ABC, abstractmethod


class IPersistencia(ABC):
    @abstractmethod
    def salvar(self, objeto, caminho):
        """Grava um objeto no caminho solicitado."""

    @abstractmethod
    def carregar(self, caminho):
        """Le os dados armazenados no caminho solicitado."""
