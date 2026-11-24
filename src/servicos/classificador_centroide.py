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
        for x, y in zip(*amostras):
            #x recebe as duas primeria características
            #y recebe as duas segundas características
            media_x = sum(x) / 2
            media_y = sum(y) / 2 
            return [(media_x, media_y)]