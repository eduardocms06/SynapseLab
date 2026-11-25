import unittest

from src.excecoes import (
    SynapseLabError,
    DimensoesIncompativeisError,
    ModeloNaoTreinadoError,
    DadoInvalidoError,
    PersistenciaError,
    HiperparametroInvalidoError
)


class TestExcecoes(unittest.TestCase):

    def test_excecao_principal(self):
        erro = SynapseLabError("Erro no projeto")
        self.assertIsInstance(erro, Exception)

    def test_dimensoes_incompativeis(self):
        self.assertTrue(
            issubclass(DimensoesIncompativeisError, SynapseLabError)
        )

    def test_modelo_nao_treinado(self):
        self.assertTrue(
            issubclass(ModeloNaoTreinadoError, SynapseLabError)
        )

    def test_dado_invalido(self):
        self.assertTrue(
            issubclass(DadoInvalidoError, SynapseLabError)
        )

    def test_persistencia(self):
        self.assertTrue(
            issubclass(PersistenciaError, SynapseLabError)
        )

    def test_hiperparametro_invalido(self):
        self.assertTrue(
            issubclass(HiperparametroInvalidoError, SynapseLabError)
        )


if __name__ == "__main__":
    unittest.main()