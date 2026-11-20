import csv
import json
from pathlib import Path

# Provisorio ate a Leticia disponibilizar a excecao oficial.
try:
    from src.excecoes import PersistenciaError
except ImportError:
    class PersistenciaError(Exception):
        pass


def salvar_json(dados, caminho):
    """Transforma dados em JSON e grava em um arquivo."""
    try:
        # Validar antes de abrir, preservando o arquivo se os dados forem invalidos.
        texto = json.dumps(dados, indent=4, ensure_ascii=False)
        caminho = Path(caminho)
        caminho.parent.mkdir(parents=True, exist_ok=True)

        with open(caminho, "w", encoding="utf-8") as arquivo:
            arquivo.write(texto)
    except (OSError, TypeError, ValueError) as erro:
        raise PersistenciaError(f"Erro ao salvar JSON: {erro}") from erro


def carregar_json(caminho):
    """Le um arquivo JSON."""
    try:
        with open(caminho, "r", encoding="utf-8") as arquivo:
            return json.load(arquivo)
    except (OSError, UnicodeError, json.JSONDecodeError) as erro:
        raise PersistenciaError(f"Erro ao carregar JSON: {erro}") from erro


def exportar_csv(registros, caminho):
    """Exporta uma lista de dicionarios para CSV."""
    try:
        if not registros:
            raise ValueError("Nao existem registros para exportar.")

        caminho = Path(caminho)
        caminho.parent.mkdir(parents=True, exist_ok=True)

        with open(caminho, "w", newline="", encoding="utf-8") as arquivo:
            escritor = csv.DictWriter(arquivo, fieldnames=registros[0].keys())
            escritor.writeheader()
            escritor.writerows(registros)
    except (OSError, ValueError, TypeError, csv.Error) as erro:
        raise PersistenciaError(f"Erro ao exportar CSV: {erro}") from erro


def carregar_csv(caminho):
    """Le um arquivo CSV e devolve uma lista de dicionarios."""
    try:
        with open(caminho, "r", newline="", encoding="utf-8") as arquivo:
            return list(csv.DictReader(arquivo))
    except (OSError, UnicodeError, csv.Error) as erro:
        raise PersistenciaError(f"Erro ao carregar CSV: {erro}") from erro
