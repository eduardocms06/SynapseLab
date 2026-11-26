import random
import math
class Dataset:
    def __init__(self, amostras, rotulos):
        self.__amostras = amostras
        self.__rotulos = rotulos

        self.__validar_dados()

    def __validar_dados(self):
        if not isinstance(self.__amostras, list):
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
                if not isinstance(valor, (int, float)) or isinstance(valor, bool):
                    raise ValueError("As características devem ser numéricas.")

                if not math.isfinite(valor):
                    raise ValueError("As características devem possuir valores finitos.")

    @property
    def amostras(self):
        return [amostra.copy() for amostra in self.__amostras]

    @property
    def rotulos(self):
        return self.__rotulos.copy()

    @property
    def quantidade_amostras(self):
        return len(self.__amostras)

    @property
    def quantidade_caracteristicas(self):
        return len(self.__amostras[0])  

    def __len__(self):
        return len(self.__amostras) #Retorna a quantidade de amostras do Dataset.

    def __getitem__(self, indice):
        return self.__amostras[indice].copy(), self.__rotulos[indice]

    def __str__(self):
        return (
            f"Dataset com {len(self)} amostras "
            f"e {self.quantidade_caracteristicas} caracteristicas "
        )

    def __repr__(self):
        return (
            f"Dataset(amostras={len(self)}, "
            f"caracteristicas={self.quantidade_caracteristicas})"
        )

    def dividir_treino_teste(self, proporcao_teste=0.2, embaralhar=True):
        if not isinstance(embaralhar, bool):
            raise TypeError("O parâmetro embaralhar deve ser booleano.")

        if not isinstance(proporcao_teste, (int,float)) or isinstance(proporcao_teste, bool):
            raise TypeError("A proporção deve ser um número.")

        if not 0 < proporcao_teste < 1:
            raise ValueError("A proporção deve estar entre 0 e 1.")

        if len(self.amostras) < 2:
            raise ValueError("O Dataset precisa ter pelo menos duas amostras.")

        indices = list(range(len(self.__amostras)))

        if embaralhar:
            random.shuffle(indices)

        quantidade_teste = max(
            1,
            min(len(indices) - 1, int(len(indices) * proporcao_teste))
        )

        indices_teste = indices[:quantidade_teste]
        indices_treino = indices[quantidade_teste:]

        # Separar amostras e rótulos
        X_treino = [self.__amostras[i].copy() for i in indices_treino]
        y_treino = [self.__rotulos[i] for i in indices_treino]

        X_teste = [self.__amostras[i].copy() for i in indices_teste]
        y_teste = [self.__rotulos[i] for i in indices_teste]

        # Criar dois novos objetos Dataset
        dataset_treino = Dataset(X_treino, y_treino)
        dataset_teste = Dataset(X_teste, y_teste)

        return dataset_treino, dataset_teste


import random
import math
class Dataset:
    def __init__(self, amostras, rotulos):
        self.__amostras = amostras
        self.__rotulos = rotulos

        self.__validar_dados()

    def __validar_dados(self):
        if not isinstance(self.__amostras, list):
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
                if not isinstance(valor, (int, float)) or isinstance(valor, bool):
                    raise ValueError("As características devem ser numéricas.")

                if not math.isfinite(valor):
                    raise ValueError("As características devem possuir valores finitos.")

    @property
    def amostras(self):
        return [amostra.copy() for amostra in self.__amostras]

    @property
    def rotulos(self):
        return self.__rotulos.copy()

    @property
    def quantidade_amostras(self):
        return len(self.__amostras)

    @property
    def quantidade_caracteristicas(self):
        return len(self.__amostras[0])  

    def __len__(self):
        return len(self.amostras) #Retorna a quantidade de amostras do Dataset.

    def __getitem__(self, indice):
        return self.__amostras[indice].copy(), self.__rotulos[indice]

    def __str__(self):
        return (
            f"Dataset com {len(self)} amostras "
            f"e {self.quantidade_caracteristicas} caracteristicas "
        )

    def __repr__(self):
        return (
            f"Dataset(amostras={len(self)}, "
            f"caracteristicas={self.quantidade_caracteristicas})"
        )

    def dividir_treino_teste(self, proporcao_teste=0.2, embaralhar=True):
        if not isinstance(embaralhar, bool):
            raise TypeError("O parâmetro embaralhar deve ser booleano.")

        if not isinstance(proporcao_teste, (int,float)) or isinstance(proporcao_teste, bool):
            raise TypeError("A proporção deve ser um número.")

        if not 0 < proporcao_teste < 1:
            raise ValueError("A proporção deve estar entre 0 e 1.")

        if len(self.__amostras) < 2:
            raise ValueError("O Dataset precisa ter pelo menos duas amostras.")

        indices = list(range(len(self.__amostras)))

        if embaralhar:
            random.shuffle(indices)

        quantidade_teste = max(
            1,
            min(len(indices) - 1, int(len(indices) * proporcao_teste))
        )

        indices_teste = indices[:quantidade_teste]
        indices_treino = indices[quantidade_teste:]

        # Separar amostras e rótulos
        X_treino = [self.__amostras[i].copy() for i in indices_treino]
        y_treino = [self.__rotulos[i] for i in indices_treino]

        X_teste = [self.__amostras[i].copy() for i in indices_teste]
        y_teste = [self.__rotulos[i] for i in indices_teste]

        # Criar dois novos objetos Dataset
        dataset_treino = Dataset(X_treino, y_treino)
        dataset_teste = Dataset(X_teste, y_teste)

        return dataset_treino, dataset_teste