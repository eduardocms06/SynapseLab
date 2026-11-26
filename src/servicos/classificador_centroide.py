from src.dominio.modelo_base import ModeloBase
import math
from typing import Any
class ClassificadorCentroide(ModeloBase):
    """Calcula o ponto médio de uma classe, por exemplo, se Gato tem duas amostras: [2.0, 10.0] e [4.0, 20.0]
        O centroide de Gato é a média de cada coluna [3.0, 15.0]"""
    
    def __init__(self, nome= "Classificador Centroide"):
        super().__init__(nome)
        self.__centroides = {}
        
    @property
    def centroide(self) -> dict[Any, list[float]]:
        return self.__centroides
    
    def __calcular_centroides(self, amostras: list[list[float]]) -> list[float]:    
        """ '*amostras' é equivalente a: (2.0, 4.0) e (10.0, 20.0) de [[2.0, 10.0], [4.0, 20.0]]
            sendo usado para reunir elementos pela posição em uma tupla com a ajuda de zip"""
        ponto_centroide = []
        for coluna in zip(*amostras):
            #coluna irá receber (1º posição, 2º posição) a cada rodada do for
            media = sum(coluna) / len(coluna)
            ponto_centroide.append(media)
        return ponto_centroide
    
    def treinar(self, X: list[list[float]], y: list[Any]) -> None:
        self._validar_dados_treino(X,y)
        self.__centroides = {}                              #reinicio do dicionario
        grupos = {}                                         #Dicionário temporário para separar as amostras
        
        for amostra, rotulo in zip(X, y):
            if rotulo not in grupos:
                grupos[rotulo] = []                         #abre uma lista a partir do rotulo se não houver nenhum em grupo
            grupos[rotulo].append(amostra)                  #Adiciona a amostra na lista de rotulo
            
        for rotulo, amostra_classe in grupos.items():
            ponto_centroide = self.__calcular_centroides(amostra_classe)                    #calcula o centroide de cada "pasta" amostra_classe
            self.__centroides[rotulo] = ponto_centroide                                     #Adiciona o ponto médio de cada amostra em self.__centroide
            
        self._treinado = True
        
    def prever(self, x: list[list[float]]) -> list[Any]:
        self._garantir_treinado()
        
        previsoes = []
        for amostra in x:
            
            distancia_amostra = []
            for classe, ponto_centroide in self.__centroides.items():                       #Anda por cada classe e ponto_centroide calculado dentro de self.__centroides
                
                resultados = []
                #Calcula as distâncias entre a amostra e o ponto_centroide
                for a, b in zip(amostra, ponto_centroide):
                    resultados.append((a-b)**2)
                    
                soma = sum(resultados)
                #Adiciona a tupla (distancia, classe) dentro da lista de distancia da amostra
                distancia_amostra.append((math.sqrt(soma), classe))
            
            menor_par = min(distancia_amostra)
            previsoes.append(menor_par[1])
        return previsoes
            
    def __str__(self) -> str:
        """Representação amigável do estado atual do modelo para o usuário."""
        
        status = "Treinado" if self.treinado else "Não treinado"
        if self.treinado:
            classes = list(self.__centroides.keys())
            return (
                f"{self.nome} (Status: {status}, "
                f"Classes aprendidas: {classes})"
            )
        return f"{self.nome} (Status: {status})"
            
    def __repr__(self) -> str:
            """Representação do objeto para depuração."""
            return (
                f"ClassificadorCentroide(nome='{self.nome}', "
                f"treinado={self.treinado}, "
                f"qtd_centroides={len(self.__centroides)})"
            )   
                