from src.dominio.modelo_base import ModeloBase
import math
from typing import Any
class ClassificadorKNN(ModeloBase):
    def __init__(self,nome = "ClassificadorKNN", k = 3):
        super().__init__(nome)
        self.k = k                                      #Quantidade de vizinhos a serem lidos
        self.__x_treino = None                          #Dados de treino guardados
        self.__y_treino = None                          #Rótulos de treinos guardados
        
    @property
    def k(self) -> int:
        """ Leitura do valor passado para K número de vizinhos configurado"""
        return self.__k
    
    @k.setter
    def k(self, valor: int) -> None:
        """ Verificação se o valor de K definido é válido antes de sua instanciação."""
        if not isinstance(valor, int) or valor <= 0:
            raise ValueError("K deve ser um número inteiro positivo.")
        self.__k = valor
        
    #Obs: Foi utilizado IA nessa parte para auxiliar na construção dos métodos de treino, previsão e calculo da distância euclidiana.
    
    def treinar(self, X: list[list[float]], y: list[Any]) -> None:
        self._validar_dados_treino(X, y)
        self.__x_treino = X
        self.__y_treino = y
        self._treinado = True
    
    def __calcular_distancia_euclidiana(self, p1: list[float], p2: list[float]) -> float:
        """Distância euclidiana é a distância entre dois pontos no espaço através de uma linha reta"""
        resultados = []
        for a, b in zip(p1, p2):
            resultados.append((a - b) ** 2)
        soma = sum(resultados)
        return math.sqrt(soma)
       
    @property
    def qtd_amostras_treinadas(self) -> int:
        if self.__x_treino is None:
            return 0
        else:
            return len(self.__x_treino)
    
    def prever(self, x: list[list[float]]) -> list[Any]:
        #Chama o método da classe mãe para fazer a verificação
        self._garantir_treinado()
        
        resultados = []
        for amostras in x:                                                          #Pega as amostras em X para fazer os cálculos necessários de previsão da IA

            lista_de_pares = []
            for indice, ponto_de_treino in enumerate(self.__x_treino):
                dist = self.__calcular_distancia_euclidiana(amostras, ponto_de_treino)
                lista_de_pares.append((dist, indice))
            
            distancia_ordenada = sorted(lista_de_pares, key=lambda par: par[0])     #Ordena os pares, para poder fazer com que as distância mais próximas sejam vizinhas.
            k_vizinhos = distancia_ordenada[: self.__k]                             #Pega somente os K vizinhos mais próximos. fatiando a lista do ínicio até K
            rotulos = [self.__y_treino[i] for _, i in k_vizinhos]                   #Pega somente os índices para buscar no y_treino os valores dos índices buscados ignorando a distância.
            vencedor = self._votar_majoritario(rotulos)                        #Conta a frequência de cada item da lista, pega o primeiro lugar depois pega a primeira posição da tupla.
            resultados.append(vencedor)
            
        return resultados
    
    def __str__(self) -> str:
        """descrever sobre o estado de um objeto atual para o usuário"""
        
        status = "Treinado" if self.__x_treino is not None else "Não treinado"
        return f"ClassificadorKNN (k = {self.k}), Status = {status}"
    
    def __repr__(self) -> str:
        """usado para depuração, facilitando a visualização da configuração do projeto."""
        
        return f"ClassificadorKNN(k = {self.k})"