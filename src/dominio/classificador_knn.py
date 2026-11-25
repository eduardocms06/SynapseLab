from modelo_base import IModelo
import math
from collections import Counter
class ClassificadorKNN(IModelo):
    def __init__(self, k = 3):
        self.k = k                                      #Quantidade de vizinhos a serem lidos
        self.__x_treino = None                          #Dados de treino guardados
        self.__y_treino = None                          #Rótulos de treinos guardados
        
    @property
    def k(self):
        """ Leitura do valor passado para K """
        return self.__k
    
    @k.setter
    def k(self, valor):
        """ Verificação se o valor de K definido é válido antes de sua instanciação."""
        if not isinstance(valor, int) or valor <= 0:
            raise ValueError("K deve ser um número inteiro positivo.")
        self.__k = valor
        
    #Obs: Foi utilizado IA nessa parte para auxiliar na construção dos métodos de treino, previsão e calculo da distância euclidiana.
    
    def treinar(self, X, y):
        if len(X) != len(y):
            raise ValueError
        
        self.__x_treino = X
        self.__y_treino = y
    
    def __calcular_distancia_euclidiana(self, p1, p2):
        """Distância euclidiana é a distância entre dois pontos no espaço através de uma linha reta"""
        resultados = []
        for a, b in zip(p1, p2):
            resultados.append((a - b) ** 2)
        soma = sum(resultados)
        return math.sqrt(soma)   
    
    def prever(self, X):
        if self.__x_treino is None:
            raise ValueError("O modelo ainda não tem nenhum treinamento, favor chamar treinar() antes de prever()")
        resultados = []
        for amostras in X:

            lista_de_pares = []
            for indice, ponto_de_treino in enumerate(self.__x_treino):
                dist = self.__calcular_distancia_euclidiana(amostras, ponto_de_treino)
                lista_de_pares.append((dist, indice))
            
            distancia_ordenada = sorted(lista_de_pares, key=lambda par: par[0])     #Ordena os pares, para poder fazer com que as distância mais próximas sejam vizinhas.
            k_vizinhos = distancia_ordenada[: self.__k]                             #Pega somente os K vizinhos mais próximos. fatiando a lista do ínicio até K
            rotulos = [self.__y_treino[i] for _, i in k_vizinhos]                   #Pega somente os índices para buscar no y_treino os valores dos índices buscados ignorando a distância.
            vencedor = Counter(rotulos).most_common(1)[0][0]
            resultados.append(vencedor)
            
        return resultados
    
    def __str__(self):
        """Dunder method para descrever amigávelmente e légivel sobre o estado de um objeto atual para o usuário"""
        
        status = "Treinado" if self.__x_treino is not None else "Não treinado"
        return f"ClassificadorKNN (k = {self.k}), Status = {status}"
    
    def __repr__(self):
        """Dunder method usado para depuração, facilitando a visualização da configuração do projeto."""
        
        return f"ClassificadorKNN(k = {self.k})"
