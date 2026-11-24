from src.dominio.modelo_base import ModeloBase

class ClassificadorCentroide(ModeloBase):
    """Calcula o ponto médio de uma classe, por exemplo, se Gato tem duas amostras: [2.0, 10.0] e [4.0, 20.0]
        O centroide de Gato é a média de cada coluna [3.0, 15.0]"""
    
    def __init__(self, nome= "Classificador Centroide"):
        super().__init__(nome)
        self.__centroides = {}
        
    @property
    def centroide(self):
        return self.__centroides
    
    def __calcular_centroides(self, amostras):
        """ '*amostras' é equivalente a: (2.0, 4.0) e (10.0, 20.0) de [[2.0, 10.0], [4.0, 20.0]]
            sendo usado para reunir elementos pela posição em uma tupla com a ajuda de zip"""
        ponto_centroide = []
        for coluna in zip(*amostras):
            #coluna irá receber (1º posição, 2º posição) a cada rodada do for
            media = sum(coluna) / len(coluna)
            ponto_centroide.append(media)
        return ponto_centroide
    
    def treinar(self, X, y):
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