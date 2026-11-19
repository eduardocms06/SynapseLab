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
    
class ModeloBase(IModelo):
    """Classe abstrata, herdando de IModelo, implementado aquilo que é comum a todos os classificadores."""
    def __init__(self, nome):
        super().__init__()
        self._treinado = False
        self._nome = nome
    #Leitura dos parâmetros 
    @property
    def treinado(self):
            return self._treinado
    @property
    def nome(self):
        return self._nome
    #Verifica se os dados estão corretos, se o tamanho de X e y são iguais.
    def _validar_dados_treino(self, X, y):
        if len(X) != len(y):
            raise ValueError("Os dados para treinamento são inválidos")
    
    #O raise ValueError é somente temporário até a criação das Exceções.
    def _garantir_treinado(self):
        if not self.treinado:
            raise ValueError("O modelo ainda não foi treinado.")
    #Texto amigável a ser mostrado para o usuário para identificar o nome do modelo e se o mesmo está treinado ou não através de True ou False.
    def __str__(self):
        return f"Modelo: {self.nome}, Modelo treinado ({self._treinado})"
    #Texto de verificação para os desenvolvedores, mostrando a representação da classe ao ser chamada.
    def __repr__(self):
        return f"ModeloBase(nome = '{self.nome}', treinado = {self._treinado})"        