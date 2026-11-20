from src.servicos.classificador_knn import ClassificadorKNN
from src.servicos.concorrencia import executar_treinamentos
from src.servicos.sessao import SessaoTreinamento
from src.persistencia.armazenamento import salvar_json, exportar_csv


class Experimento:
    """Treina e compara diferentes valores de K usando threads."""

    def __init__(self, X_treino, y_treino, X_teste, y_teste, valores_k=(1, 3, 5)):
        if not X_treino or not X_teste:
            raise ValueError("Os conjuntos nao podem estar vazios.")
        if len(X_treino) != len(y_treino):
            raise ValueError("Treino: X e y possuem tamanhos diferentes.")
        if len(X_teste) != len(y_teste):
            raise ValueError("Teste: X e y possuem tamanhos diferentes.")

        # Uma tupla permite verificar e reutilizar ate mesmo geradores.
        valores_k = tuple(valores_k)
        if not valores_k:
            raise ValueError("Informe pelo menos um valor de K.")
        for k in valores_k:
            if type(k) is not int or k <= 0 or k % 2 == 0 or k > len(X_treino):
                raise ValueError(f"Valor de K invalido: {k}")

        self.X_treino = X_treino
        self.y_treino = y_treino
        self.X_teste = X_teste
        self.y_teste = y_teste
        self.valores_k = valores_k

    def _treinar_e_avaliar(self, k):
        """Cada thread treina seu proprio modelo e calcula a acuracia."""
        modelo = ClassificadorKNN(k=k)
        modelo.treinar(self.X_treino, self.y_treino)
        previsoes = modelo.prever(self.X_teste)

        acertos = sum(real == previsto for real, previsto in zip(self.y_teste, previsoes))
        return {"modelo": "KNN", "k": k, "acuracia": acertos / len(self.y_teste)}

    def executar(self):
        with SessaoTreinamento("Experimento KNN") as sessao:
            historico = executar_treinamentos(self.valores_k, self._treinar_e_avaliar)

        resultados = sorted(historico.obter_resultados(), key=lambda item: item["k"])
        # Se as acuracias forem iguais, escolhe o menor K.
        melhor = max(resultados, key=lambda item: (item["acuracia"], -item["k"]))

        return {
            "resultados": resultados,
            "melhor_modelo": melhor,
            "tempo_total": sessao.tempo_total
        }

    def salvar_relatorios(self, relatorio):
        salvar_json(relatorio, "resultados/relatorio_experimento.json")
        exportar_csv(relatorio["resultados"], "resultados/relatorio_experimento.csv")
