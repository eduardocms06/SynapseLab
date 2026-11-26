
import unittest

from src.servicos.classificador_knn import ClassificadorKNN

class TestClassificadorKNN(unittest.TestCase):

    def test_criar_classificador(self):
        modelo = ClassificadorKNN(k=3)
        self.assertEqual(modelo.k, 3)

    def test_alterar_k(self):
        modelo = ClassificadorKNN()
        modelo.k = 5
        self.assertEqual(modelo.k, 5)

    def test_k_zero_deve_gerar_erro(self):
        with self.assertRaises(ValueError):
            ClassificadorKNN(k=0)

    def test_k_negativo_deve_gerar_erro(self):
        with self.assertRaises(ValueError):
            ClassificadorKNN(k=-1)

    def test_k_decimal_deve_gerar_erro(self):
        with self.assertRaises(ValueError):
            ClassificadorKNN(k=2.5)

    def test_k_texto_deve_gerar_erro(self):
        with self.assertRaises(ValueError):
            ClassificadorKNN(k="3")

    def test_treinar_com_tamanhos_diferentes(self):
        modelo = ClassificadorKNN()
        with self.assertRaises(ValueError):
            modelo.treinar([[1, 2], [3, 4]], ["A"])

    def test_prever_sem_treinar(self):
        modelo = ClassificadorKNN()
        with self.assertRaises(ValueError):
            modelo.prever([[1, 2]])

    def test_treinar_e_prever(self):
        modelo = ClassificadorKNN(k=1)
        modelo.treinar([[1, 2], [8, 9]], ["A", "B"])

        resultado = modelo.prever([[1, 3]])

        self.assertEqual(resultado, ["A"])

    def test_prever_retorna_lista(self):
        modelo = ClassificadorKNN(k=1)
        modelo.treinar([[1, 2], [8, 9]], ["A", "B"])

        resultado = modelo.prever([[1, 3]])

        self.assertIsInstance(resultado, list)

    def test_str_mostra_status(self):
        modelo = ClassificadorKNN()
        self.assertIn("Não treinado", str(modelo))

    def test_repr_mostra_configuracao(self):
        modelo = ClassificadorKNN(k=3)
        self.assertEqual(repr(modelo), "ClassificadorKNN(k = 3)")


if __name__ == "__main__":
    unittest.main()
