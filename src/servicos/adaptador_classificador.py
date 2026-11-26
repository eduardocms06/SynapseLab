
from typing import Any

from src.dominio.modelo_base import IModelo


class AdaptadorClassificador(IModelo):
    """
    Adapta modelos externos à interface do SynapseLab.
    """

    def __init__(self, modelo_externo: Any):
        self._modelo_externo = modelo_externo

        if (
            callable(getattr(modelo_externo, "ajustar", None))
            and callable(getattr(modelo_externo, "classificar", None))
        ):
            self._metodo_treinar = modelo_externo.ajustar
            self._metodo_prever = modelo_externo.classificar

        elif (
            callable(getattr(modelo_externo, "fit", None))
            and callable(getattr(modelo_externo, "predict", None))
        ):
            self._metodo_treinar = modelo_externo.fit
            self._metodo_prever = modelo_externo.predict

        else:
            raise TypeError(
                "Modelo externo não possui métodos compatíveis."
            )

    def treinar(self, X: list[list[float]], y: list) -> None:
        self._metodo_treinar(X, y)

    def prever(self, x: list[list[float]]) -> list:
        return self._metodo_prever(x)

    def nome_modelo(self) -> str:
        return f"Adaptador de {type(self._modelo_externo).__name__}"
