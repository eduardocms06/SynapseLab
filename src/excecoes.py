
class SynapseLabError(Exception):
    """Exceção principal do projeto SynapseLab."""
    def __init__(self, mensagem: str) -> None:
        self.mensagem = mensagem
        super().__init__(mensagem)


class DimensoesIncompativeisError(SynapseLabError):
    """Erro quando as dimensões dos dados são incompatíveis."""
    pass


class ModeloNaoTreinadoError(SynapseLabError):
    """Erro quando o modelo ainda não foi treinado."""
    pass


class DadoInvalidoError(SynapseLabError):
    """Erro quando um dado informado é inválido."""
    pass


class PersistenciaError(SynapseLabError):
    """Erro ao salvar ou carregar dados."""
    pass


class HiperparametroInvalidoError(SynapseLabError):
    """Erro quando um hiperparâmetro é inválido."""
    pass

class ConcorrenciaError(SynapseLabError):
    """Erro em execuções paralelas ou falhas em threads."""
    pass