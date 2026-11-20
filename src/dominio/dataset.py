class Dataset:
    def __init__(self, amostras, rotulos):
        self.__amostras = amostras
        self.__rotulos = rotulos

        self.__validar_dados()

    def __validar_dados(self):
        if not isinstance(self.amostras, list):
            raise TypeError("As amostras devem ser uma lista.")

        if not isinstance(self.__rotulos, list):
            raise TypeError("Os rótulos devem ser uma lista.")

        if len(self.__amostras) != len(self.__rotulos):
            raise ValueError(
                "A quantidade de amostras deve ser igual à quantidade de rótulos."
            )

        if len(self.__amostras) == 0:
            raise ValueError("O Dataset não pode estar vazio.")

        quantidade_caracteristica = len(self.__amostras[0])

        if quantidade_caracteristica == 0:
            raise ValueError("As amostras devem possuir caracteristicas")

        for amostra in self.__amostras:
            if not isinstance(amostra, list):
                raise TypeError("Cada amostra deve ser uma lista")

            if len(amostra) != quantidade_caracteristica:
                raise ValueError("Todas as amostras devem possuir a mesma dimensão.")

            for valor in amostra:
                if not isinstance(valor,(int, float)) or isinstance(valor, bool):
                    raise ValueError("As características devem ser numéricas.")
                