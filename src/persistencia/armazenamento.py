
import csv
import json
from pathlib import Path

try:
    from src.excecoes import PersistenciaError
except ImportError:
    class PersistenciaError(Exception):
        """Excecao temporaria para erros de persistencia."""
        pass


def salvar_json(dados, caminho):
    """Salva dados em um arquivo JSON."""
    try:
        caminho = Path(caminho)
        caminho.parent.mkdir(parents=True, exist_ok=True)

        with open(caminho, "w", encoding="utf-8") as arquivo:
            json.dump(dados, arquivo, indent=4, ensure_ascii=False)

    except (OSError, TypeError, ValueError) as erro:
        raise PersistenciaError(
            f"Erro ao salvar JSON: {erro}"
        ) from erro


def carregar_json(caminho):
    """Carrega dados de um arquivo JSON."""
    try:
        with open(caminho, "r", encoding="utf-8") as arquivo:
            return json.load(arquivo)

    except (OSError, UnicodeError, json.JSONDecodeError) as erro:
        raise PersistenciaError(
            f"Erro ao carregar JSON: {erro}"
        ) from erro


def exportar_csv(registros, caminho):
    """Exporta uma lista de dicionarios para CSV."""
    try:
        if not registros:
            raise ValueError("Nao existem registros para exportar.")

        colunas = list(registros[0].keys())

        caminho = Path(caminho)
        caminho.parent.mkdir(parents=True, exist_ok=True)

        with open(caminho, "w", newline="", encoding="utf-8") as arquivo:
            escritor = csv.DictWriter(
                arquivo,
                fieldnames=colunas
            )

            escritor.writeheader()
            escritor.writerows(registros)

    except (OSError, ValueError, TypeError, csv.Error) as erro:
        raise PersistenciaError(
            f"Erro ao exportar CSV: {erro}"
        ) from erro


def carregar_csv(caminho):
    """Carrega registros de um arquivo CSV."""
    try:
        with open(caminho, "r", newline="", encoding="utf-8") as arquivo:
            leitor = csv.DictReader(arquivo)
            return list(leitor)

    except (OSError, UnicodeError, csv.Error) as erro:
        raise PersistenciaError(
            f"Erro ao carregar CSV: {erro}"
        ) from erro
