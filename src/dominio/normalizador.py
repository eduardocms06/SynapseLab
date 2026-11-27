
import math

from src.dominio.transformadores import Transformador


class Normalizador(Transformador):

    def __init__(self):
        self.__minimos = []
        self.__maximos = []
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

                if not isinstance(valor, (int, float)) or isinstance(valor, bool):
                    raise ValueError("As características devem ser numéricas.")

                if not math.isfinite(valor):
                    raise ValueError("As características devem possuir valores finitos.")

        self.__minimos = []
        self.__maximos = []

        for coluna in range(quantidade_caracteristicas):

            valores = [amostra[coluna] for amostra in X]

            self.__minimos.append(min(valores))
            self.__maximos.append(max(valores))

        self.__ajustado = True

    def transformar(self, X):

        if not self.__ajustado:
            raise RuntimeError("O normalizador precisa ser ajustado antes da transformação.")

        if not isinstance(X, list) or len(X) == 0:
            raise ValueError("Os dados devem ser uma lista não vazia.")

        quantidade_caracteristicas = len(self.__minimos)

        resultado = []

        for amostra in X:

            if not isinstance(amostra, list):
                raise TypeError("Cada amostra deve ser uma lista.")

            if len(amostra) != quantidade_caracteristicas:
                raise ValueError("A quantidade de características é incompatível.")

            nova_amostra = []

            for coluna in range(quantidade_caracteristicas):

                valor = amostra[coluna]

                if not isinstance(valor, (int, float)) or isinstance(valor, bool):
                    raise ValueError("As características devem ser numéricas.")

                if not math.isfinite(valor):
                    raise ValueError("As características devem possuir valores finitos.")

                minimo = self.__minimos[coluna]
                maximo = self.__maximos[coluna]

                if maximo == minimo:
                    valor_normalizado = 0.0
                else:
                    valor_normalizado = (valor - minimo) / (maximo - minimo)

                nova_amostra.append(valor_normalizado)

            resultado.append(nova_amostra)

        return resultado
