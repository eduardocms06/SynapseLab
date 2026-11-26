from abc import ABC, abstractmethod

class Transformador(ABC):
    @abstractmethod
    def ajustar(self, X):
        pass

    @abstractmethod
    def transformar(self, X):
        pass
    
    def ajustar_e_transformar(self, X):
        self.ajustar(X)
        return self.transformar(X)
    