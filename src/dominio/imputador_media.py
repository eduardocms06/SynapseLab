import math

from src.dominio.transformadores import Transformador


class ImputadorMedia(Transformador):

    def __init__(self):
        self.__medias = []
        self.__ajustado = False

    def ajustar(self, X):

        self.__ajustado = False

        if not isinstance(X, list) or len(X) == 0:
            raise ValueError("Os dados devem ser uma lista não vazia.")

        if not isinstance(X[0], list):
            raise TypeError("Cada amostra deve ser uma lista.")

        quantidade_caracteristicas = len(X[0])

        if quantidade_caracteristicas == 0:
            raise ValueError("As amostras devem possuir características.")

        for amostra in X:

            if not isinstance(amostra, list):
                raise TypeError("Cada amostra deve ser uma lista.")

            if len(amostra) != quantidade_caracteristicas:
                raise ValueError("Todas as amostras devem possuir a mesma dimensão.")

            for valor in amostra:

                if valor is not None:

                    if not isinstance(valor, (int, float)) or isinstance(valor, bool):
                        raise ValueError("As características devem ser numéricas ou None.")

                    if not math.isfinite(valor):
                        raise ValueError("As características devem possuir valores finitos.")

        self.__medias = []

        for coluna in range(quantidade_caracteristicas):

            valores = [
                amostra[coluna]
                for amostra in X
                if amostra[coluna] is not None
            ]

            if len(valores) == 0:
                raise ValueError("Não é possível calcular a média de uma coluna totalmente vazia.")

            media = sum(valores) / len(valores)

            self.__medias.append(media)

        self.__ajustado = True

    def transformar(self, X):

        if not self.__ajustado:
            raise RuntimeError("O imputador precisa ser ajustado antes da transformação.")

        if not isinstance(X, list) or len(X) == 0:
            raise ValueError("Os dados devem ser uma lista não vazia.")

        quantidade_caracteristicas = len(self.__medias)

        resultado = []

        for amostra in X:

            if not isinstance(amostra, list):
                raise TypeError("Cada amostra deve ser uma lista.")

            if len(amostra) != quantidade_caracteristicas:
                raise ValueError("A quantidade de características é incompatível.")

            nova_amostra = []

            for coluna in range(quantidade_caracteristicas):

                valor = amostra[coluna]

                if valor is None:
                    valor = self.__medias[coluna]

                elif not isinstance(valor, (int, float)) or isinstance(valor, bool):
                    raise ValueError("As características devem ser numéricas ou None.")

                elif not math.isfinite(valor):
                    raise ValueError("As características devem possuir valores finitos.")

                nova_amostra.append(valor)

            resultado.append(nova_amostra)

        return resultado