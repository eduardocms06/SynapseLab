from typing import Any
class Metrica:
    """A classe métrica deve conter seus métodos como estáticos, sendo utilizada para consultar cálculos,
    funciona como módulo utilitário dispensando parâmetros self. permitindo chamadas diretas."""
    
    #Foi utilizado LLm nessa parte do trabalho para ajudar a identificar o que seria necessário e começar a estruturar um pouco a lógica
    #de cada etapa, sem gerar o código completo. Utilizei para descobrir como é o cálculo de método da classe 
    #e como verificar os vp, fp e fn
    
    @staticmethod
    def _validar_listas(y_real: list, y_pred: list) -> None:
        if len(y_real) != len(y_pred):
            raise ValueError("As listas possuem dimensões diferentes.")
    
    @staticmethod
    def _contar_resultados(y_real: list, y_pred: list, classe_pos: Any)-> tuple[int, int, int]:
        """Calcula verdadeiros positivos, falso positivos e falsos negativos para a classe positiva informada"""
        vp = 0
        fp = 0
        fn = 0
        
        for real, pred in zip(y_real, y_pred):
            if real == classe_pos and pred == classe_pos:
                vp +=1
            #Quando o modelo chuta a classe positiva mas erra 
            elif real != classe_pos and pred == classe_pos:         
                fp +=1
            elif real == classe_pos and pred != classe_pos:
                fn +=1
        
        return vp, fp, fn
         
    @staticmethod
    def calcular_acuracia(y_real: list, y_pred: list) -> float:
        """Calcula a proporção de predições corretas sobre o total."""
        Metrica._validar_listas(y_real, y_pred)     
           
        if not y_real:
            return 0.0
        
        #Soma-se 1 para cada vez que real for igual à predição
        acertos = sum( 1 for real, pred in zip(y_real, y_pred) if real == pred)
        return acertos / len(y_real)
    
    @staticmethod
    def calcular_precisao(y_real: list, y_pred: list, classe_pos: Any) -> float:
        """Calcula a precisão para a classe positiva informada, através da divisão entre quantidade de verdadeiros positivos
            dividido pela quantidade de verd. pos. + falsos positivos"""
            
        Metrica._validar_listas(y_real, y_pred) 
        vp, fp, _ = Metrica._contar_resultados(y_real, y_pred, classe_pos)
        
        if (vp + fp) == 0:
            return 0.0
        
        return vp / (vp + fp)
    
    @staticmethod
    def calcular_revocacao(y_real: list, y_pred: list, classe_pos: Any) -> float:
        """Calcula o Recall para a classe positiva informada, por vp / vp + fn"""
        
        Metrica._validar_listas(y_real, y_pred)
        
        vp, _, fn = Metrica._contar_resultados(y_real, y_pred, classe_pos)
        
        if (vp + fn) == 0:
            return 0.0 
        return vp / (vp + fn)  
    
    @staticmethod
    def calcular_f1(y_real: list, y_pred: list, classe_pos: Any) -> float:
        """Calcula a média harmônica entre precisão e revocação"""
        
        Metrica._validar_listas(y_real, y_pred)
        precisao = Metrica.calcular_precisao(y_real, y_pred, classe_pos) 
        revocacao = Metrica.calcular_revocacao(y_real, y_pred, classe_pos)
        
        if (precisao + revocacao) == 0:
            return 0.0
        return 2* (precisao * revocacao) / (precisao + revocacao) 
    
    @staticmethod
    def matriz_confusao(y_real: list, y_pred: list) -> dict:
        """Tabela de cruzamento de dados usada para diagnosticar onde e como um classificador errou ou acertou
        ela abre os resultados por categoria, mostrando qual classificador esrá errando mais."""
        
        Metrica._validar_listas(y_real, y_pred)
        if not y_real:
            return {}
        
        try:
            #Obtém todas as classes únicas e ordenadas
            classes = sorted(set(y_real) | set(y_pred))
        except TypeError:
            # cria um dicionário com os itens da lista como chaves, mantendo a ordem de execução e retirando duplicidades.
            classes = list(dict.fromkeys(y_real + y_pred))
            
        #Prepara a estrutura da matriz com um dicionário de dicionário preenchendo todas as combinações possíveis entre reais e preditas com 0
        matriz = {
            real: {pred: 0 for pred in classes}
            for real in classes
        }
        #Pareia os elementos das duas listas posição por posição acessando a chave externa real(linha) e a interna pred(coluna) somando 1
        for real, pred in zip(y_real, y_pred):
            matriz[real][pred] += 1
            
        return matriz