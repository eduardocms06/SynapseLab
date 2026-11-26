"""Armazena resultados e coordena avaliacoes utilizando threads."""
import threading
import time
from copy import deepcopy

from src.dominio.resultado_execucao import ResultadoExecucao
from src.padroes.configuracao_global import ConfiguracaoGlobal


class HistoricoExecucao:
    """Colecao de resultados protegida com Lock."""

    def __init__(self):
        self.__registros = []
        self.__trava = threading.Lock()

    @property
    def registros(self):
        return self.obter_resultados()

    @property
    def melhor_resultado(self):
        ranking = self.obter_ranking()
        return ranking[0] if ranking else None

    def registrar(self, resultado):
        """Registra um ResultadoExecucao; aceita dicts legados por compatibilidade."""
        if not isinstance(resultado, (ResultadoExecucao, dict)):
            raise TypeError("O registro deve ser um ResultadoExecucao ou dict.")
        with self.__trava:
            self.__registros.append(deepcopy(resultado))

    def obter_ranking(self):
        def nota(item):
            if isinstance(item, ResultadoExecucao):
                return (item.acuracia, -item.tempo_segundos)
            return (item.get("acuracia", -1), -item.get("tempo_segundos", 0))

        return sorted(self.obter_resultados(), key=nota, reverse=True)

    def __len__(self):
        with self.__trava:
            return len(self.__registros)

    def __getitem__(self, idx):
        with self.__trava:
            return deepcopy(self.__registros[idx])

    def __str__(self):
        return f"HistoricoExecucao({len(self)} registros)"

    def registrar_resultado(self, resultado):
        self.registrar(resultado)

    def obter_resultados(self):
        with self.__trava:
            return deepcopy(self.__registros)

    def quantidade_resultados(self):
        return len(self)


class AvaliadorConcorrente:
    """Executa modelos ou folds em threads com um limite de workers."""

    def __init__(self, max_workers=None):
        if max_workers is None:
            max_workers = ConfiguracaoGlobal().max_workers
        if type(max_workers) is not int or max_workers < 1:
            raise ValueError("max_workers deve ser inteiro positivo.")
        self.__max_workers = max_workers
        self.__trava = threading.Lock()

    @property
    def max_workers(self):
        return self.__max_workers

    def _executar_etapa_com_lock(self, modelo, dados_treino, dados_teste, historico,
                                fold=None, ao_evento=None):
        """Treina uma copia do modelo e registra seu resultado."""
        X_treino, y_treino = dados_treino
        X_teste, y_teste = dados_teste
        if not X_treino or not X_teste or len(X_treino) != len(y_treino) or len(X_teste) != len(y_teste):
            raise ValueError("Dados de treino ou teste invalidos.")

        modelo_independente = deepcopy(modelo)
        inicio = time.perf_counter()
        modelo_independente.treinar(X_treino, y_treino)
        previsoes = modelo_independente.prever(X_teste)
        tempo = time.perf_counter() - inicio
        if len(previsoes) != len(y_teste):
            raise ValueError("O modelo retornou uma quantidade incorreta de previsoes.")
        acuracia = sum(a == b for a, b in zip(previsoes, y_teste)) / len(y_teste)

        nome = getattr(modelo_independente, "nome_modelo", None)
        nome = nome() if callable(nome) else type(modelo_independente).__name__
        detalhes = {}
        if fold is not None:
            detalhes["fold"] = fold
        if hasattr(modelo_independente, "k"):
            detalhes["k"] = modelo_independente.k
        registro = ResultadoExecucao(nome, acuracia, tempo, detalhes)
        # Trava do avaliador protege esta secao; historico tambem protege sua lista.
        with self.__trava:
            historico.registrar(registro)
        if ao_evento is not None:
            ao_evento({"tipo": "etapa_concluida", "resultado": registro.para_dict(),
                       "fold": fold})
        return registro

    def _executar_em_threads(self, tarefas, parada_solicitada=None):
        """Espera cada lote e nao inicia outros quando a parada e solicitada."""
        erros = []

        def rodar(tarefa):
            try:
                if parada_solicitada is None or not parada_solicitada():
                    tarefa()
            except Exception as erro:
                with self.__trava:
                    erros.append(erro)

        for inicio in range(0, len(tarefas), self.__max_workers):
            if parada_solicitada is not None and parada_solicitada():
                break
            lote = tarefas[inicio:inicio + self.__max_workers]
            threads = [threading.Thread(target=rodar, args=(t,)) for t in lote]
            for thread in threads:
                thread.start()
            for thread in threads:
                thread.join()
        if erros:
            raise RuntimeError("Falha em uma ou mais avaliacoes concorrentes.") from erros[0]

    def comparar_modelos_paralelo(self, modelos, dataset, historico, *, dados_divididos=None,
                                  ao_evento=None, parada_solicitada=None):
        """Avalia modelos com Dataset ou com dados de treino/teste ja preparados."""
        if dados_divididos is None:
            treino, teste = dividir_dataset(dataset)
        else:
            treino, teste = dados_divididos
        tarefas = [
            (lambda modelo=modelo: self._executar_etapa_com_lock(
                modelo, treino, teste, historico, ao_evento=ao_evento))
            for modelo in modelos
        ]
        self._executar_em_threads(tarefas, parada_solicitada)
        return historico

    def validar_cruzada_paralela(self, modelo, dataset, k_folds, historico, *,
                                ao_evento=None, parada_solicitada=None, dados_arrays=None):
        """Valida o modelo em folds disjuntos e notifica o fim de cada fold."""
        X, y = dados_arrays if dados_arrays is not None else obter_arrays(dataset)
        if type(k_folds) is not int or not 2 <= k_folds <= len(X):
            raise ValueError("k_folds deve estar entre 2 e a quantidade de amostras.")
        tarefas = []
        for i in range(k_folds):
            idx_teste = set(range(i, len(X), k_folds))
            treino = ([X[j] for j in range(len(X)) if j not in idx_teste],
                      [y[j] for j in range(len(y)) if j not in idx_teste])
            teste = ([X[j] for j in range(len(X)) if j in idx_teste],
                     [y[j] for j in range(len(y)) if j in idx_teste])
            tarefas.append(lambda treino=treino, teste=teste, fold=i: self._executar_etapa_com_lock(
                modelo, treino, teste, historico, fold=fold, ao_evento=ao_evento))
        self._executar_em_threads(tarefas, parada_solicitada)
        return historico


def obter_arrays(dataset):
    """Obtem amostras e rotulos do Dataset."""
    try:
        X, y = list(dataset.amostras), list(dataset.rotulos)
    except AttributeError as erro:
        raise TypeError("Dataset deve disponibilizar .amostras e .rotulos.") from erro
    if not X or len(X) != len(y):
        raise ValueError("Dataset vazio ou inconsistente.")
    return X, y


def dividir_dataset(dataset):
    """Aceita (DatasetTreino, DatasetTeste) ou ((Xtr,ytr),(Xte,yte))."""
    if hasattr(dataset, "dividir_treino_teste"):
        partes = dataset.dividir_treino_teste(0.2)
        if len(partes) != 2:
            raise TypeError("A divisao deve retornar (treino, teste).")
        treino, teste = partes
        if hasattr(treino, "amostras"):
            return obter_arrays(treino), obter_arrays(teste)
        if len(treino) == 2 and len(teste) == 2:
            return (list(treino[0]), list(treino[1])), (list(teste[0]), list(teste[1]))
        raise TypeError("Formato de divisao do Dataset nao reconhecido.")
    raise TypeError(
        "O Dataset precisa implementar dividir_treino_teste(proporcao_teste). "
        "Integre o Dataset do Hugo em src/dominio/dataset.py."
    )


def executar_treinamentos(valores_k, tarefa_treinamento, historico=None, *,
                          ao_resultado=None, parada_solicitada=None, max_workers=None):
    """Executa treinamentos legados e opcionalmente emite eventos por resultado."""
    if historico is None:
        historico = HistoricoExecucao()
    erros = []
    trava_erros = threading.Lock()
    valores_k = list(valores_k)
    if max_workers is None:
        max_workers = len(valores_k) or 1
    if type(max_workers) is not int or max_workers < 1:
        raise ValueError("max_workers deve ser inteiro positivo.")

    def executar_tarefa(k):
        try:
            if parada_solicitada is not None and parada_solicitada():
                return
            resultado = tarefa_treinamento(k)
            historico.registrar_resultado(resultado)
            if ao_resultado is not None:
                ao_resultado(resultado)
        except Exception as erro:
            with trava_erros:
                erros.append(erro)

    for inicio in range(0, len(valores_k), max_workers):
        if parada_solicitada is not None and parada_solicitada():
            break
        lote = valores_k[inicio:inicio + max_workers]
        threads = [threading.Thread(target=executar_tarefa, args=(k,)) for k in lote]
        for thread in threads:
            thread.start()
        for thread in threads:
            thread.join()
        if erros:
            break
    if erros:
        raise RuntimeError("Um ou mais treinamentos falharam.") from erros[0]
    return historico
