from abc import ABC, abstractmethod

class IModelo(ABC):
    """Interface que define parâmetros obrigatórios para todos os modelos do projeto."""
    
    @abstractmethod
    def treinar(self, X, y):
        """Treina o modelo com a matriz X e rótulos y"""
        pass
    
    @abstractmethod
    def prever(self, X):
        """Realiza predições para as amostras em X"""
        pass