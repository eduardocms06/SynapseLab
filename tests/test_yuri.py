
import unittest
import tempfile
from pathlib import Path

from src.servicos.concorrencia import (
    HistoricoExecucao,
    executar_treinamentos
)
from src.servicos.sessao import SessaoTreinamento
from src.persistencia.armazenamento import (
    salvar_json,
    carregar_json,
    exportar_csv,
    carregar_csv,
    PersistenciaError
)


class TestesYuri(unittest.TestCase):

    def test_historico(self):
        historico = HistoricoExecucao()
        historico.registrar_resultado({"k": 3})

        self.assertEqual(
            historico.quantidade_resultados(), 1
        )

    def test_historico_encapsulamento(self):
        historico = HistoricoExecucao()
        historico.registrar_resultado({"k": 3})

        copia = historico.obter_resultados()
        copia.clear()

        self.assertEqual(
            historico.quantidade_resultados(), 1
        )

    def test_dez_threads(self):
        def tarefa(k):
            return {"k": k}

        historico = executar_treinamentos(
            range(10), tarefa
        )

        resultados = historico.obter_resultados()

        self.assertEqual(len(resultados), 10)
        self.assertEqual(
            {item["k"] for item in resultados},
            set(range(10))
        )

    def test_sessao(self):
        with SessaoTreinamento("Teste") as sessao:
            pass

        self.assertIsNotNone(sessao.tempo_total)
        self.assertGreaterEqual(sessao.tempo_total, 0)

    def test_sessao_com_erro(self):
        sessao = SessaoTreinamento("Teste erro")

        with self.assertRaises(ValueError):
            with sessao:
                raise ValueError("Erro simulado")

        self.assertIsNotNone(sessao.tempo_total)

    def test_json(self):
        dados = [{"k": 3, "acuracia": 0.95}]

        with tempfile.TemporaryDirectory() as pasta:
            caminho = Path(pasta) / "teste.json"

            salvar_json(dados, caminho)
            resultado = carregar_json(caminho)

            self.assertEqual(dados, resultado)

    def test_csv(self):
        dados = [{"k": 3, "acuracia": 0.95}]

        with tempfile.TemporaryDirectory() as pasta:
            caminho = Path(pasta) / "teste.csv"

            exportar_csv(dados, caminho)
            resultado = carregar_csv(caminho)

            self.assertEqual(len(resultado), 1)
            self.assertEqual(resultado[0]["k"], "3")

    def test_arquivo_inexistente(self):
        with tempfile.TemporaryDirectory() as pasta:
            caminho = Path(pasta) / "inexistente.json"

            with self.assertRaises(PersistenciaError):
                carregar_json(caminho)


    def test_historico_copia_profunda(self):
        historico = HistoricoExecucao()
        registro = {"k": 3, "acuracia": 0.95}

        historico.registrar_resultado(registro)

        registro["acuracia"] = 0.10

        copia = historico.obter_resultados()
        copia[0]["acuracia"] = 0.20

        self.assertEqual(
            historico.obter_resultados()[0]["acuracia"],
            0.95
        )

    def test_gerador_vazio_experimento(self):
        from src.dominio.experimento import Experimento

        valores_k = (k for k in [])

        with self.assertRaises(ValueError):
            Experimento(
                X_treino=[[0], [1], [8]],
                y_treino=["A", "A", "B"],
                X_teste=[[0.5]],
                y_teste=["A"],
                valores_k=valores_k
            )

if __name__ == "__main__":
    unittest.main()