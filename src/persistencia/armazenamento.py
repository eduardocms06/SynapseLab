"""Permite salvar e carregar dados em JSON e CSV por classes e funcoes."""
import csv
import json
from pathlib import Path

from src.persistencia.interface import IPersistencia

try:
    from src.excecoes import PersistenciaError
except ImportError:
    class PersistenciaError(Exception):
        def __init__(self, mensagem, caminho_arquivo=""):
            self.caminho_arquivo = str(caminho_arquivo)
            super().__init__(mensagem)


def _lancar_erro(acao, caminho, erro):
    """Converte falhas de arquivo em PersistenciaError e preserva a causa."""
    mensagem = f"Erro ao {acao}: {erro}"
    try:
        excecao = PersistenciaError(mensagem, str(caminho))
    except TypeError:
        excecao = PersistenciaError(mensagem)
    raise excecao from erro


class PersistenciaJSON(IPersistencia):
    """Salva e le JSON usando with open."""

    def salvar(self, objeto, caminho):
        try:
            if hasattr(objeto, "amostras") and hasattr(objeto, "rotulos"):
                objeto = self._serializar_dataset(objeto)
            elif hasattr(objeto, "para_dict"):
                objeto = objeto.para_dict()
            # Serializa antes de abrir: dados invalidos nao apagam arquivo anterior.
            texto = json.dumps(objeto, indent=4, ensure_ascii=False)
            caminho = Path(caminho)
            caminho.parent.mkdir(parents=True, exist_ok=True)
            with open(caminho, "w", encoding="utf-8") as arquivo:
                arquivo.write(texto)
        except (OSError, TypeError, ValueError) as erro:
            _lancar_erro("salvar JSON", caminho, erro)

    def carregar(self, caminho):
        try:
            with open(caminho, "r", encoding="utf-8") as arquivo:
                dados = json.load(arquivo)
            if isinstance(dados, dict) and dados.get("__tipo__") == "Dataset":
                return self._desserializar_dataset(dados)
            return dados
        except (OSError, UnicodeError, ValueError, ImportError, TypeError) as erro:
            _lancar_erro("carregar JSON", caminho, erro)

    def _serializar_dataset(self, dataset):
        return {
            "__tipo__": "Dataset",
            "amostras": dataset.amostras,
            "rotulos": dataset.rotulos,
            "nomes_atributos": getattr(dataset, "nomes_atributos", None),
        }

    def _desserializar_dataset(self, dados):
        from src.dominio.dataset import Dataset
        nomes_atributos = dados.get("nomes_atributos")
        if nomes_atributos is None:
            return Dataset(dados["amostras"], dados["rotulos"])
        return Dataset(dados["amostras"], dados["rotulos"], nomes_atributos)


class PersistenciaCSV(IPersistencia):
    """Salva tabelas de registros e recupera as linhas como dicionarios."""

    def salvar(self, objeto, caminho):
        try:
            if hasattr(objeto, "amostras") and hasattr(objeto, "rotulos"):
                registros = []
                for amostra, rotulo in zip(objeto.amostras, objeto.rotulos):
                    linha = {f"atributo_{i+1}": valor for i, valor in enumerate(amostra)}
                    linha["rotulo"] = rotulo
                    registros.append(linha)
            else:
                registros = list(objeto)
            if not registros:
                raise ValueError("Nao existem registros para exportar.")
            if not all(isinstance(r, dict) for r in registros):
                raise TypeError("CSV exige uma lista de dicionarios.")
            colunas = list(registros[0])
            if any(set(r) != set(colunas) for r in registros):
                raise ValueError("As linhas CSV precisam ter as mesmas colunas.")
            caminho = Path(caminho)
            caminho.parent.mkdir(parents=True, exist_ok=True)
            with open(caminho, "w", newline="", encoding="utf-8") as arquivo:
                escritor = csv.DictWriter(arquivo, fieldnames=colunas)
                escritor.writeheader()
                escritor.writerows(registros)
        except (OSError, ValueError, TypeError, csv.Error) as erro:
            _lancar_erro("exportar CSV", caminho, erro)

    def carregar(self, caminho):
        try:
            with open(caminho, "r", newline="", encoding="utf-8") as arquivo:
                return list(csv.DictReader(arquivo))
        except (OSError, UnicodeError, csv.Error) as erro:
            _lancar_erro("carregar CSV", caminho, erro)


def salvar_json(dados, caminho):
    return PersistenciaJSON().salvar(dados, caminho)


def carregar_json(caminho):
    return PersistenciaJSON().carregar(caminho)


def exportar_csv(registros, caminho):
    return PersistenciaCSV().salvar(registros, caminho)


def carregar_csv(caminho):
    return PersistenciaCSV().carregar(caminho)
