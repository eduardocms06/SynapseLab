from src.dominio.modelo_base import ModeloBase
from collections import Counter

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
    
    def __str__(self):
        return 
    
    def __repr__(self):
        return 
    
    def treinar(self, X, y):
        self._validar_dados_treino(X, y)
        
        if self.__limiar == None:
            lista_peso = [linha[self.__indice_corte] for linha in X]
            limiar_medio = sum(lista_peso) / len(lista_peso)

        rotulos_acima = []
        rotulos_abaixo = []    
        for peso, rotulo in zip(X, y):
            if peso >= limiar_medio:
                rotulos_acima.append(rotulo)
            else:
                rotulos_abaixo.append(rotulo)

        self.__classe_acima = self._votar_majoritario(rotulos_acima)
        self.__classe_abaixo = self._votar_majoritario(rotulos_abaixo)
        self._treinado = True
        
    def prever(self, X):
        """Recebe os dados novos dos quais não se sabe o gabarito e consulta as regras do treino, gerando uma lista com as classes preditas
            para cada amostra recebida"""
        
        self._garantir_treinado()
        
        predicoes = []
        
        for amostra in X:
            valor = amostra[self.__indice_corte]
            
            if valor >= self.__limiar:
                predicoes.append(self.__classe_acima)
            else:
                predicoes.append(self.__classe_abaixo)
                
        return predicoes
        