from src.dominio.modelo_base import ModeloBase
from collections import Counter
from typing import Any
from src.excecoes import DadoInvalidoError, HiperparametroInvalidoError
#Foi utilizado ajuda de LLM para a criação e retiraar dúvidas sobre como fazer as regras do classificador.
class ClassificadorRegras(ModeloBase):
    """Modelo classificador simples usado somente para comparação. Se o modelo ClassificadorKNN for pior que ele, não compensa utilizar o classificador"""
    
    def __init__(self, nome = "Classificador por Regras", limiar=None, indice_corte=0):
        super().__init__(nome)
        if isinstance(indice_corte, bool) or indice_corte < 0 or not (isinstance(indice_corte, int)):
            raise HiperparametroInvalidoError(f"O valor {indice_corte} passado para o índice de corte deve ser inteiro maior ou igual a 0")
            
        self.__limiar = limiar
        self.__indice_corte = indice_corte
        self.__classe_acima = None
        self.__classe_abaixo = None
        
    @property
    def limiar(self) -> float | None:
        return self.__limiar
    
    def __str__(self) -> str:
        #Representação para o usuário
        
        status = "Treinado" if self.treinado else "Não treinado"
        
        if self.treinado:
            return (f"Classificador por Regras (Status: {status})"
                    f"Coluna de corte: {self.__indice_corte}, Limiar: {self.__limiar:.2f}"        
            )
        return (f"Classificador por Regras (Status: {status})"
                f"Coluna de corte: {self.__indice_corte}"
        )
    
    def __repr__(self) -> str:
        #Representação para depuração
        
        return (f"Classificador por Regras: {self.__limiar}"
                f"Índice de Corte: {self.__indice_corte}"        
        )
    
    def treinar(self, X: list[list[float]], y: list[Any]) -> None:
        """Método usado para a fase de aprendizado ensinando o modelo com respostas anteriores onde X são as caracteristicas e y os gabaritos
            Responsavel por encontar o __limiar e eleger quem e o 'vencedor' de cada lado (abaixo e acima)"""
        
        self._validar_dados_treino(X, y)
        
        #Se o limiar não foi fixado, calcula pela média da coluna de corte
        if self.__limiar is None:
            try: 
                lista_peso = [linha[self.__indice_corte] for linha in X]
            except IndexError as erro:
                raise DadoInvalidoError(f"índice de corte fora dos limites das colunas {len(X[0])} colunas") from erro
            
            self.__limiar = sum(lista_peso) / len(lista_peso)

        rotulos_acima = []
        rotulos_abaixo = []  
        try: 
            for amostra, rotulo in zip(X, y):
                
                if amostra[self.__indice_corte] >= self.__limiar:
                    rotulos_acima.append(rotulo)
                else:
                    rotulos_abaixo.append(rotulo)
        except IndexError as erro:
            raise DadoInvalidoError(f"índice de corte fora dos limites das colunas {len(X[0])} colunas") from erro
                
        """FallBack de segurança, contra valores absurdos no limiar, sendo aa classe padrão um 'chute' da classe mais votada em y"""
        classe_padrao = self._votar_majoritario(y)
        
        #Define rotulos_acima em __classe_acima, somente se houver item (True) o mesmo vale para __classe_abaixo  
        self.__classe_acima = self._votar_majoritario(rotulos_acima) if rotulos_acima else classe_padrao                
        self.__classe_abaixo = self._votar_majoritario(rotulos_abaixo) if rotulos_abaixo else classe_padrao
        
        self._treinado = True
        
    def prever(self, x: list[list[float]]) -> list[Any]:
        """Recebe os dados novos dos quais não se sabe o gabarito e consulta as regras do treino, gerando uma lista com as classes preditas
            para cada amostra recebida"""
        
        self._garantir_treinado()
        if not x:
            raise DadoInvalidoError("Os dados para previsão 'x' não devem estar vazios")
        predicoes = []
        try: 
            for amostra in x:
                valor = amostra[self.__indice_corte]
                
                if valor >= self.__limiar:
                    predicoes.append(self.__classe_acima)
                else:
                    predicoes.append(self.__classe_abaixo)
        except IndexError as erro:
            raise DadoInvalidoError(f"O parâmetro passado em indice_corte {self.__indice_corte} está fora dos limites das colunas")
                
        return predicoes
        