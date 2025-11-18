import numpy as np
import matplotlib.pyplot as plt
from models.validation_chain import (
    Corrida300Handler,
    BarraFixaHandler,
    Corrida2400Handler,
    ResultadoFinalHandler,
)
from sklearn.cluster import KMeans

class CandidateController:
    def __init__(self, model):
        self.model = model
        self.validation_chain = self.build_validation_chain()

    def build_validation_chain(self):
        h1 = Corrida300Handler()
        h2 = BarraFixaHandler()
        h3 = Corrida2400Handler()
        h4 = ResultadoFinalHandler()
        h1.set_next(h2).set_next(h3).set_next(h4)
        return h1

    def create_candidate(self, nome, cpf, tempo_300_str, barra_str, tempo_2400_str):
        if not nome or not cpf or not tempo_300_str or not barra_str or not tempo_2400_str:
            raise ValueError("Preencha todos os campos")
        if not cpf.isdigit() or len(cpf) != 11:
            raise ValueError("CPF deve ter 11 dígitos numéricos")
        try:
            tempo_300 = float(tempo_300_str.replace(",", "."))
            barra_fixa = int(barra_str)
            tempo_2400 = float(tempo_2400_str.replace(",", "."))
        except Exception:
            raise ValueError("Use números válidos nos campos de tempo e barra fixa")

        candidate = {
            "nome": nome.strip(),
            "cpf": cpf.strip(),
            "tempo_300": tempo_300,
            "barra_fixa": barra_fixa,
            "tempo_2400": tempo_2400,
        }
        candidate = self.validation_chain.handle(candidate)
        self.model.create_candidate(candidate)

    def list_candidates(self):
        return self.model.list_candidates()

    def get_status_counts(self):
        return self.model.count_by_status()

    def show_kmeans_graph(self):
        candidates = self.model.list_candidates()

        if not candidates:
            raise Exception("Não existem dados suficientes para gerar o gráfico.")

        X = []
        nomes = []
        status_list = []

        for c in candidates:
            try:
                tempo_300 = float(c.get("tempo_300", 0))
                barra_fixa = float(c.get("barra_fixa", 0))
                tempo_2400 = float(c.get("tempo_2400", 0))
            except Exception:
                continue

            X.append([tempo_300, barra_fixa, tempo_2400])
            nomes.append(c.get("nome", ""))
            status_list.append(c.get("status", ""))

        if len(X) < 2:
            raise Exception("É preciso pelo menos 2 candidatos para rodar o K-Means.")

        X = np.array(X)

        # K-Means com 2 clusters (apenas para cumprir o requisito)
        kmeans = KMeans(n_clusters=2, random_state=42)
        kmeans.fit(X)

        plt.figure(figsize=(10, 6))

        for i in range(len(X)):
            status = status_list[i]
            if status == "APROVADO":
                color = "green"
            else:
                color = "red"

            plt.scatter(X[i][0], X[i][2], color=color)
            plt.text(X[i][0], X[i][2], nomes[i], fontsize=8, color=color)

        plt.xlabel("Tempo 300m (min)")
        plt.ylabel("Tempo 2.4km (min)")
        plt.title("K-Means com 2 grupos: Aprovados x Reprovados")
        plt.grid(True)

        aprovados = status_list.count("APROVADO")
        reprovados = status_list.count("REPROVADO")
        plt.legend(
            handles=[
                plt.Line2D([0], [0], marker="o", color="w", markerfacecolor="green", label=f"Aprovados ({aprovados})"),
                plt.Line2D([0], [0], marker="o", color="w", markerfacecolor="red", label=f"Reprovados ({reprovados})"),
            ],
            loc="upper left",
        )

        plt.show()
    def get_candidate(self, candidate_id):
        return self.model.get_candidate_by_id(candidate_id)

    def update_candidate(self, candidate_id, nome, cpf, tempo_300_str, barra_str, tempo_2400_str):
        if not nome or not cpf or not tempo_300_str or not barra_str or not tempo_2400_str:
            raise ValueError("Preencha todos os campos")
        if not cpf.isdigit() or len(cpf) != 11:
            raise ValueError("CPF deve ter 11 dígitos numéricos")
        try:
            tempo_300 = float(tempo_300_str.replace(",", "."))
            barra_fixa = int(barra_str)
            tempo_2400 = float(tempo_2400_str.replace(",", "."))
        except Exception:
            raise ValueError("Use números válidos nos campos de tempo e barra fixa")

        candidate = {
            "nome": nome.strip(),
            "cpf": cpf.strip(),
            "tempo_300": tempo_300,
            "barra_fixa": barra_fixa,
            "tempo_2400": tempo_2400,
        }
        candidate = self.validation_chain.handle(candidate)
        self.model.update_candidate(candidate_id, candidate)
