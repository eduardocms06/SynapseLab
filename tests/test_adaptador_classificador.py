
import unittest

from src.servicos.adaptador_classificador import AdaptadorClassificador
from src.dominio.modelo_base import IModelo


class ModeloExterno:
    def ajustar(self, X, y):
        self.treinado = True

    def classificar(self, X):
        return ["A"] * len(X)


class ModeloFitPredict:
    def fit(self, X, y):
        self.treinado = True

    def predict(self, X):
        return ["B"] * len(X)


class ModeloIncompativel:
    pass


class TestAdaptadorClassificador(unittest.TestCase):

    def test_implementa_interface(self):
        adaptador = AdaptadorClassificador(ModeloExterno())
        self.assertIsInstance(adaptador, IModelo)

    def test_adaptar_ajustar_classificar(self):
        adaptador = AdaptadorClassificador(ModeloExterno())
        adaptador.treinar([[1, 2]], ["A"])
        self.assertEqual(adaptador.prever([[3, 4]]), ["A"])

    def test_adaptar_fit_predict(self):
        adaptador = AdaptadorClassificador(ModeloFitPredict())
        adaptador.treinar([[1, 2]], ["B"])
        self.assertEqual(adaptador.prever([[3, 4]]), ["B"])

    def test_modelo_incompativel(self):
        with self.assertRaises(TypeError):
            AdaptadorClassificador(ModeloIncompativel())

    def test_nome_modelo(self):
        adaptador = AdaptadorClassificador(ModeloExterno())
        self.assertEqual(adaptador.nome_modelo(), "Adaptador de ModeloExterno")


if __name__ == "__main__":
    unittest.main()
