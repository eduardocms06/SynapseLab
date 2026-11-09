from modelo_base import IModelo

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
        
    def treinar(self, X, y):
        pass
    
    def prever(self, X):
        pass
    
    def __str__(self):
        """Dunder method para descrever amigávelmente e légivel sobre o estado de um objeto atual para o usuário"""
        
        status = "Treinado" if self.__x_treino is not None else "Não treinado"
        return f"ClassificadorKNN (k = {self.k}), Status = {status}"
    
    def __repr__(self):
        """Dunder method usado para depuração, facilitando a visualização da configuração do projeto."""
        
        return f"ClassificadorKNN(k = {self.k})"