"""Coordena experimentos com modelos, historico e avaliacao concorrente."""
import json
from copy import deepcopy
from pathlib import Path
import threading

from src.persistencia.armazenamento import PersistenciaCSV, PersistenciaJSON
from src.padroes.configuracao_global import ConfiguracaoGlobal
from src.padroes.observador_treino import IObservadorTreino
from src.servicos.concorrencia import (
    AvaliadorConcorrente, HistoricoExecucao,
    dividir_dataset, executar_treinamentos,
)
from src.servicos.sessao import SessaoTreinamento
from src.servicos.classificador_knn import ClassificadorKNN


class Experimento:
    """Coordena Dataset, modelos, avaliador, historico e persistencia."""

    def __init__(self, titulo="Experimento", dataset=None, transformador=None,
                 *, X_treino=None, y_treino=None, X_teste=None, y_teste=None,
                 valores_k=(1, 3, 5)):
        self.__titulo = titulo
        self.__dataset = dataset
        self.__transformador = transformador
        self.__modelos = []
        self.__historico = HistoricoExecucao()
        self.__avaliador = AvaliadorConcorrente()
        self.__tempo_total = None
        self.__configuracao = ConfiguracaoGlobal()
        self.__observadores = []
        self.__trava_observadores = threading.Lock()
        self.__parada = threading.Event()
        self.__modo_legado = X_treino is not None

        if self.__modo_legado:
            if not X_treino or not X_teste:
                raise ValueError("Os conjuntos nao podem estar vazios.")
            if len(X_treino) != len(y_treino) or len(X_teste) != len(y_teste):
                raise ValueError("X e y possuem tamanhos diferentes.")
            valores_k = tuple(valores_k)
            if not valores_k:
                raise ValueError("Informe pelo menos um valor de K.")
            if any(type(k) is not int or k <= 0 or k % 2 == 0 or k > len(X_treino)
                   for k in valores_k):
                raise ValueError("Valor de K invalido.")
            self.__dados_legados = (X_treino, y_treino, X_teste, y_teste, valores_k)
        elif dataset is None:
            raise ValueError("Informe um Dataset para o experimento.")

    @property
    def titulo(self):
        return self.__titulo

    @property
    def dataset(self):
        return self.__dataset

    @property
    def historico(self):
        return self.__historico

    @property
    def modelos(self):
        return self.__modelos.copy()

    def inscrever(self, observador):
        """Inscreve um observador sem duplicar a mesma instancia."""
        if not isinstance(observador, IObservadorTreino):
            raise TypeError("O observador deve implementar IObservadorTreino.")
        with self.__trava_observadores:
            if observador in self.__observadores:
                return False
            self.__observadores.append(observador)
            return True

    def remover(self, observador):
        """Remove um observador previamente inscrito."""
        with self.__trava_observadores:
            if observador not in self.__observadores:
                return False
            self.__observadores.remove(observador)
            return True

    def notificar(self, evento):
        """Avisa os observadores fora do Lock e recolhe pedidos de parada."""
        mensagem = {"titulo": self.__titulo, **evento}
        with self.__trava_observadores:
            observadores = self.__observadores.copy()
        for observador in observadores:
            observador.atualizar(deepcopy(mensagem))
            if observador.parada_solicitada:
                self.__parada.set()

    @property
    def parada_solicitada(self):
        return self.__parada.is_set()

    def _notificar_fim(self):
        if self.__parada.is_set():
            self.notificar({"tipo": "parada_antecipada", "total_resultados": len(self.__historico)})
        self.notificar({"tipo": "fim_experimento", "total_resultados": len(self.__historico),
                        "tempo_total": self.__tempo_total})

    def adicionar_modelo(self, modelo):
        if not callable(getattr(modelo, "treinar", None)) or not callable(getattr(modelo, "prever", None)):
            raise TypeError("O modelo precisa ter treinar(X, y) e prever(X).")
        self.__modelos.append(modelo)

    def _dados_para_avaliacao(self):
        treino, teste = dividir_dataset(self.__dataset)
        if self.__transformador is not None:
            transformador = deepcopy(self.__transformador)
            X_treino = transformador.ajustar_e_transformar(treino[0])
            X_teste = transformador.transformar(teste[0])
            treino = X_treino, treino[1]
            teste = X_teste, teste[1]
        return treino, teste

    def _avaliar(self, concorrente):
        if self.__modo_legado:
            raise RuntimeError("Use executar() para experimentos no formato antigo.")
        if not self.__modelos:
            raise ValueError("Adicione ao menos um modelo antes de executar.")
        self.__historico = HistoricoExecucao()
        self.__tempo_total = None
        self.__parada.clear()
        try:
            self.notificar({"tipo": "inicio_experimento"})
            dados = self._dados_para_avaliacao()
            avaliador = self.__avaliador if concorrente else AvaliadorConcorrente(max_workers=1)
            with SessaoTreinamento(self.__titulo) as sessao:
                avaliador.comparar_modelos_paralelo(
                    self.__modelos, self.__dataset, self.__historico,
                    dados_divididos=dados,
                    ao_evento=self.notificar,
                    parada_solicitada=self.__parada.is_set,
                )
            self.__tempo_total = sessao.tempo_total
            self._notificar_fim()
            return self.__historico
        except Exception as erro:
            self.notificar({"tipo": "erro_experimento", "erro": str(erro)})
            raise

    def executar_avaliacao_sequencial(self):
        return self._avaliar(concorrente=False)

    def executar_avaliacao_concorrente(self):
        return self._avaliar(concorrente=True)

    def gerar_relatorio_final(self):
        """Gera texto JSON com os resultados armazenados."""
        melhor = self.__historico.melhor_resultado
        dados = {
            "titulo": self.__titulo,
            "resultados": [r.para_dict() for r in self.__historico.registros],
            "melhor_modelo": melhor.para_dict() if melhor else None,
            "tempo_total": self.__tempo_total,
        }
        return json.dumps(dados, ensure_ascii=False, indent=4)

    def executar(self):
        if not self.__modo_legado:
            self.executar_avaliacao_concorrente()
            return json.loads(self.gerar_relatorio_final())

        X_treino, y_treino, X_teste, y_teste, valores_k = self.__dados_legados

        def avaliar_k(k):
            modelo = ClassificadorKNN(k=k)
            modelo.treinar(X_treino, y_treino)
            previsoes = modelo.prever(X_teste)
            acuracia = sum(a == b for a, b in zip(previsoes, y_teste)) / len(y_teste)
            return {"modelo": "KNN", "k": k, "acuracia": acuracia}

        self.__parada.clear()
        self.__tempo_total = None
        self.__historico = HistoricoExecucao()
        try:
            self.notificar({"tipo": "inicio_experimento"})
            with SessaoTreinamento("Experimento KNN") as sessao:
                executar_treinamentos(
                    valores_k, avaliar_k, self.__historico,
                    ao_resultado=lambda resultado: self.notificar({
                        "tipo": "etapa_concluida",
                        "resultado": {"nome_modelo": "KNN", **resultado},
                    }),
                    parada_solicitada=self.__parada.is_set,
                    max_workers=self.__avaliador.max_workers,
                )
            self.__tempo_total = sessao.tempo_total
            resultados = sorted(self.__historico.obter_resultados(), key=lambda r: r["k"])
            melhor = max(resultados, key=lambda r: (r["acuracia"], -r["k"]))
            self._notificar_fim()
            return {"resultados": resultados, "melhor_modelo": melhor,
                    "tempo_total": self.__tempo_total}
        except Exception as erro:
            self.notificar({"tipo": "erro_experimento", "erro": str(erro)})
            raise

    def salvar_relatorios(self, relatorio=None):
        if relatorio is None:
            relatorio = json.loads(self.gerar_relatorio_final())
        diretorio = Path(self.__configuracao.diretorio_saida)
        PersistenciaJSON().salvar(relatorio, diretorio / "relatorio_experimento.json")
        PersistenciaCSV().salvar(relatorio["resultados"],
                                 diretorio / "relatorio_experimento.csv")
