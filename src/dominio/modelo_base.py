from abc import ABC, abstractmethod
from collections import Counter
from typing import Any
from src.excecoes import DimensoesIncompativeisError
from src.excecoes import ModeloNaoTreinadoError
class IModelo(ABC):
    """Interface que define parâmetros obrigatórios para todos os modelos do projeto."""
    
    @abstractmethod
    def treinar(self, X: list[list[float]], y: list) -> None:
        """Treina o modelo com a matriz X e rótulos y"""
        pass
    
    @abstractmethod
    def prever(self, x: list[list[float]]) -> list:
        """Realiza predições para as amostras em X"""
        pass
    
    @abstractmethod
    def nome_modelo(self) -> str:
        #Nome de identificação do modelo
        pass
class ModeloBase(IModelo):
    """Classe abstrata, herdando de IModelo, implementado aquilo que será comum em todos os classificadores."""
    def __init__(self, nome):
        super().__init__()
        self._treinado = False
        self._nome = nome
        
    #Leitura dos parâmetros    
    @property    
    def nome(self) -> str:
        return self._nome
    
    @property
    def treinado(self) -> bool:
            return self._treinado
    
    def nome_modelo(self) -> str:
        #Retorna o nome definido na instanciação do __init__ de modeloBase
        return self._nome
    
    #Decidir alterar _votar_majoritário para ModeloBase, pois mais de um modelo utiliza esse método, facilitando assim a sua utilização
    def _votar_majoritario(self, lista: list[Any]) -> Any:
        return Counter(lista).most_common(1)[0][0]
        
    #Verifica se os dados estão corretos, se o tamanho de X e y são iguais.
    def _validar_dados_treino(self, X: list[list[float]], y: list[Any]):
        if len(X) != len(y):
            raise DimensoesIncompativeisError(
                f"Os vetores informados são imcompatíveis {len(X)} é diferente de {len(y)}"
            )
    
    #O raise ValueError é somente temporário até a criação das Exceções.
    def _garantir_treinado(self) -> None:
        if not self.treinado:
            raise ModeloNaoTreinadoError(
                f" O modelo {self.nome_modelo} ainda não foi treinado. Status: {self.treinado}"
            )
        
    #Texto ser mostrado para o usuário identificar o nome do modelo e se ele está treinado ou não através de True ou False.
    def __str__(self) -> str:
        return f"Modelo: {self.nome}, Modelo treinado ({self._treinado})"
    
    #Texto de verificação para os desenvolvedores, mostrando a representação da classe ao ser chamada.
    def __repr__(self):
        return f"ModeloBase(nome = '{self.nome}', treinado = {self._treinado})"        