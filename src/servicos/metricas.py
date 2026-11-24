class Metrica:
    """A classe métrica deve conter seus métodos como estáticos, sendo utilizada para consultar cálculos,
    funciona como módulo utilitário dispensando parâmetros self. permitindo chamadas diretas."""
    @staticmethod
    def _validar_listas(y_real, y_pred):
        if len(y_real) != len(y_pred):
            raise ValueError("As listas possuem dimensões diferentes.")
        
    @staticmethod
    def calcular_acuracia(y_real, y_pred):
        """Calcula a proporção de predições corretas sobre o total."""
        Metrica._validar_listas()
        
        if not y_real:
            return 0.0
        
        #Soma-se 1 para cada vez que real for igual à predição
        acertos = sum( 1 for real, pred in zip(y_real, y_pred) if real == pred)
        return acertos / len(y_real)