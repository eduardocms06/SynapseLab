
from src.servicos.classificador_knn import ClassificadorKNN
from src.servicos.concorrencia import executar_treinamentos
from src.servicos.sessao import SessaoTreinamento
from src.persistencia.armazenamento import salvar_json, exportar_csv


class Experimento:
    """Orquestra a avaliacao concorrente de modelos KNN."""

    def __init__(
        self,
        X_treino,
        y_treino,
        X_teste,
        y_teste,
        valores_k=(1, 3, 5)
    ):
        if not X_treino or not X_teste:
            raise ValueError("Os conjuntos nao podem estar vazios.")

        if len(X_treino) != len(y_treino):
            raise ValueError("Treino: X e y possuem tamanhos diferentes.")

        if len(X_teste) != len(y_teste):
            raise ValueError("Teste: X e y possuem tamanhos diferentes.")

        if not valores_k:
            raise ValueError("Informe pelo menos um valor de K.")

        
        # Converter para tupla antes de validar
        valores_k = tuple(valores_k)

        # Verificar se existem valores
        if not valores_k:
            raise ValueError(
                "Informe pelo menos um valor de K."
            )

        # Validar cada valor de K
        for k in valores_k:
            if not isinstance(k, int) or isinstance(k, bool):
                raise ValueError(
                    "K deve ser um numero inteiro."
                )

            if k <= 0 or k % 2 == 0 or k > len(X_treino):
                raise ValueError(
                    f"Valor de K invalido: {k}"
                )


        self.X_treino = X_treino
        self.y_treino = y_treino
        self.X_teste = X_teste
        self.y_teste = y_teste
        self.valores_k = valores_k

    def _treinar_e_avaliar(self, k):
        """Treina um modelo independente e calcula a acuracia."""

        modelo = ClassificadorKNN(k=k)
        modelo.treinar(self.X_treino, self.y_treino)

        previsoes = modelo.prever(self.X_teste)

        acertos = sum(
            real == previsto
            for real, previsto in zip(self.y_teste, previsoes)
        )

        acuracia = acertos / len(self.y_teste)

        return {
            "modelo": "KNN",
            "k": k,
            "acuracia": acuracia
        }

    def executar(self):
        """Executa os treinamentos e organiza os resultados."""

        with SessaoTreinamento("Experimento KNN") as sessao:
            historico = executar_treinamentos(
                valores_k=self.valores_k,
                tarefa_treinamento=self._treinar_e_avaliar
            )

        resultados = sorted(
            historico.obter_resultados(),
            key=lambda item: item["k"]
        )

        # Em caso de empate, escolhe o menor K
        melhor = max(
            resultados,
            key=lambda item: (item["acuracia"], -item["k"])
        )

        return {
            "resultados": resultados,
            "melhor_modelo": melhor,
            "tempo_total": sessao.tempo_total
        }

    def salvar_relatorios(self, relatorio):
        """Salva os resultados em JSON e CSV."""

        salvar_json(
            relatorio,
            "resultados/relatorio_experimento.json"
        )

        exportar_csv(
            relatorio["resultados"],
            "resultados/relatorio_experimento.csv"
        )
