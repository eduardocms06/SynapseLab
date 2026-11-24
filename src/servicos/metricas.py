class Metrica:
    """A classe métrica deve conter seus métodos como estáticos, sendo utilizada para consultar cálculos,
    funciona como módulo utilitário dispensando parâmetros self. permitindo chamadas diretas."""
    
    #Foi utilizado LLm nessa parte do trabalho para ajudar a identificar o que seria necessário e começar a estruturar um pouco a lógica
    #de cada etapa, sem gerar o código completo. Utilizei para descobrir como é o cálculo de método da classe 
    #e como verificar os vp, fp e fn
    
    @staticmethod
    def _validar_listas(y_real, y_pred):
        if len(y_real) != len(y_pred):
            raise ValueError("As listas possuem dimensões diferentes.")
    
    @staticmethod
    def _contar_resultados(y_real, y_pred, classe_pos):
        """Calcula verdadeiros positivos, falso positivos e falsos negativos para a classe positiva informada"""
        vp = 0
        fp = 0
        fn = 0
        if y_real == classe_pos and y_pred == classe_pos:
            vp +=1
        #Quando o modelo chuta a classe positiva mas erra 
        elif y_real != classe_pos and y_pred == classe_pos:         
            fp +=1
        elif y_real == classe_pos and y_pred != classe_pos:
            fn +=1
         
    @staticmethod
    def calcular_acuracia(y_real, y_pred):
        """Calcula a proporção de predições corretas sobre o total."""
        Metrica._validar_listas()
        
        if not y_real:
            return 0.0
        
        #Soma-se 1 para cada vez que real for igual à predição
        acertos = sum( 1 for real, pred in zip(y_real, y_pred) if real == pred)
        return acertos / len(y_real)
    
    @staticmethod
    def calcular_precisao(y_real, y_pred, classe_pos):
        """Calcula a precisão para a classe positiva informada, através da divisão entre quantidade de verdadeiros positivos
            dividido pela quantidade de verd. pos. + falsos positivos"""
            
        Metrica._validar_listas(y_real, y_pred) 
        vp, fp, _ = Metrica._contar_resultados(y_real, y_pred, classe_pos)
        
        if (vp + fp) == 0:
            return 0.0
        
        return vp / (vp + fp)
    
    @staticmethod
    def calcular_revocacao(y_real, y_pred, classe_pos):
        """Calcula o Recall para a classe positiva informada, por vp / vp + fn"""
        
        Metrica._validar_listas(y_real, y_pred)
        
        vp, _, fn = Metrica._contar_resultados(y_real, y_pred, classe_pos)
        
        if (vp + fn) == 0:
            return 0.0 
        return vp / (vp + fn)  
    
    def calcular_f1(y_real, y_pred, classe_pos):
        """Calcula a média harmônica entre precisão e revocação"""
        
        Metrica._validar_listas(y_real, y_pred)
        precisao = Metrica.calcular_precisao(y_real, y_pred, classe_pos) 
        revocacao = Metrica.calcular_revocacao(y_real, y_pred, classe_pos)
        
        if (precisao + revocacao) == 0:
            return 0.0
        return 2* (precisao * revocacao) / (precisao + revocacao) 