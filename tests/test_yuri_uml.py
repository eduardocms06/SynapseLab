"""Testa sessao, historico, avaliador, experimento e persistencia."""
import tempfile
import unittest
from pathlib import Path

from src.dominio.resultado_execucao import ResultadoExecucao
from src.persistencia.armazenamento import PersistenciaCSV, PersistenciaJSON, PersistenciaError
from src.persistencia.interface import IPersistencia
from src.servicos.classificador_knn import ClassificadorKNN
from src.servicos.concorrencia import AvaliadorConcorrente, HistoricoExecucao
from src.servicos.sessao import SessaoTreinamento


class TestesArquiteturaUML(unittest.TestCase):
    def test_sessao_sucesso_erro(self):
        with SessaoTreinamento("Normal") as sessao:
            pass
        self.assertTrue(sessao.sucesso)
        self.assertIsNotNone(sessao.tempo_total)
        sessao_erro = SessaoTreinamento("Falha")
        with self.assertRaises(ValueError):
            with sessao_erro:
                raise ValueError("Falha simulada")
        self.assertFalse(sessao_erro.sucesso)

    def test_resultado_e_historico_uml(self):
        historico = HistoricoExecucao()
        fraco = ResultadoExecucao("KNN", 0.7, 0.1, {"k": 1})
        forte = ResultadoExecucao("KNN", 0.9, 0.2, {"k": 3})
        historico.registrar(fraco)
        historico.registrar(forte)
        self.assertEqual(len(historico), 2)
        self.assertEqual(historico.melhor_resultado, forte)
        self.assertEqual(historico.obter_ranking()[0], forte)
        reg = historico[0]
        self.assertEqual(reg.acuracia, 0.7)
        self.assertIn("2 registros", str(historico))

    def test_interface_e_persistencia(self):
        with self.assertRaises(TypeError):
            IPersistencia()
        self.assertIsInstance(PersistenciaJSON(), IPersistencia)
        self.assertIsInstance(PersistenciaCSV(), IPersistencia)
        with tempfile.TemporaryDirectory() as pasta:
            caminho = Path(pasta)
            registros = [{"modelo": "KNN", "k": 1, "acuracia": 1.0}]
            PersistenciaJSON().salvar(registros, caminho / "dados.json")
            self.assertEqual(PersistenciaJSON().carregar(caminho / "dados.json"), registros)
            PersistenciaCSV().salvar(registros, caminho / "dados.csv")
            self.assertEqual(PersistenciaCSV().carregar(caminho / "dados.csv")[0]["k"], "1")

    def test_csv_registros_inconsistentes(self):
        with tempfile.TemporaryDirectory() as pasta:
            with self.assertRaises(PersistenciaError):
                PersistenciaCSV().salvar([{"a": 1}, {"b": 2}], Path(pasta)/"teste.csv")
            self.assertFalse((Path(pasta)/"teste.csv").exists())

    def test_avaliador_multiplos_modelos(self):
        treino = ([[0], [1], [2], [3], [8], [9], [10], [11]],
                  ["A"] * 4 + ["B"] * 4)
        teste = ([[0.5], [9.5]], ["A", "B"])
        historico = HistoricoExecucao()
        avaliador = AvaliadorConcorrente(max_workers=2)
        avaliador.comparar_modelos_paralelo(
            [ClassificadorKNN(k=1), ClassificadorKNN(k=3)],
            None, historico, dados_divididos=(treino, teste),
        )
        self.assertEqual(len(historico), 2)
        self.assertTrue(all(isinstance(r, ResultadoExecucao) for r in historico.registros))
        self.assertTrue(all(r.acuracia == 1.0 for r in historico.registros))


if __name__ == "__main__":
    unittest.main()
