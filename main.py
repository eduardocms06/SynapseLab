
from src.dominio.experimento import Experimento


def executar_experimento():
    """Executa a comparacao de modelos KNN."""

    X_treino = [
        [0], [0.5], [1], [1.5],
        [8], [8.5], [9], [9.5]
    ]

    y_treino = [
        "A", "A", "A", "A",
        "B", "B", "B", "B"
    ]

    X_teste = [[0.2], [1.2], [8.2], [9.2]]
    y_teste = ["A", "A", "B", "B"]

    experimento = Experimento(
        X_treino=X_treino,
        y_treino=y_treino,
        X_teste=X_teste,
        y_teste=y_teste,
        valores_k=[1, 3, 5]
    )

    relatorio = experimento.executar()

    print("\nRESULTADOS DOS TREINAMENTOS")

    for resultado in relatorio["resultados"]:
        print(
            f"K={resultado['k']} | "
            f"Acuracia={resultado['acuracia']:.2%}"
        )

    melhor = relatorio["melhor_modelo"]

    print("\nMELHOR CONFIGURACAO:")
    print(f"K = {melhor['k']}")
    print(f"Acuracia = {melhor['acuracia']:.2%}")

    experimento.salvar_relatorios(relatorio)

    print("\nRelatorios JSON e CSV salvos!")
    print(f"Tempo total: {relatorio['tempo_total']:.4f}s")


def main():
    while True:
        print("\n" + "=" * 40)
        print("          SYNAPSELAB")
        print("=" * 40)
        print("1 - Executar experimento KNN")
        print("0 - Sair")

        opcao = input("\nEscolha uma opcao: ")

        if opcao == "1":
            executar_experimento()

        elif opcao == "0":
            print("Encerrando SynapseLab...")
            break

        else:
            print("Opcao invalida. Tente novamente.")


if __name__ == "__main__":
    main()
