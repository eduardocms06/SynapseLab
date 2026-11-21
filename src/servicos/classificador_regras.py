from src.dominio.modelo_base import ModeloBase

#Foi utilizado ajuda de LLM para a criação e dúvidas sobre como fazer as regras do classificador.
class ClassificadorRegras(ModeloBase):
    """Modelo classificador simples usado somente para comparação. Se o modelo ClassificadorKNN for pior que ele, não compensa utilizar o classificador"""
    
    def __init__(self, limiar=None, indice_corte=0):
        super().__init__(nome="Classificador por Regras")
        self.__limiar = limiar
        self.__indice_corte = indice_corte
        self.__classe_acima = None
        self.__classe_abaixo = None
        
    @property
    def limiar(self):
        return self.__limiar
    