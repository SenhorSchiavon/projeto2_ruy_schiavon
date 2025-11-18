import tkinter as tk
from tkinter import ttk, messagebox

class MainView(ttk.Frame):
    def __init__(self, master, controller):
        super().__init__(master)
        self.controller = controller

        self.nome_var = tk.StringVar()
        self.cpf_var = tk.StringVar()
        self.tempo300_var = tk.StringVar()
        self.barra_var = tk.StringVar()
        self.tempo2400_var = tk.StringVar()

        self.aprovados_var = tk.StringVar(value="0")
        self.reprovados_var = tk.StringVar(value="0")

        self.selected_candidate_id = None

        self.build_ui()
        self.refresh_table()
        self.refresh_stats()

    def build_ui(self):
        self.pack(fill="both", expand=True, padx=12, pady=12)

        top_frame = ttk.Frame(self)
        top_frame.pack(fill="both", expand=True, pady=(0, 12))

        self.tree = ttk.Treeview(
            top_frame,
            columns=("nome", "cpf", "t300", "barra", "t2400", "status"),
            show="headings",
            height=8,
        )
        self.tree.heading("nome", text="Nome")
        self.tree.heading("cpf", text="CPF")
        self.tree.heading("t300", text="300m (min)")
        self.tree.heading("barra", text="Barra Fixa")
        self.tree.heading("t2400", text="2.4km (min)")
        self.tree.heading("status", text="Status")
        self.tree.column("nome", width=160)
        self.tree.column("cpf", width=100)
        self.tree.column("t300", width=90, anchor="center")
        self.tree.column("barra", width=90, anchor="center")
        self.tree.column("t2400", width=110, anchor="center")
        self.tree.column("status", width=90, anchor="center")
        self.tree.pack(fill="both", expand=True)

        self.tree.bind("<<TreeviewSelect>>", self.on_row_select)

        form_frame = ttk.LabelFrame(self, text="Candidato")
        form_frame.pack(fill="x", pady=(0, 12))

        ttk.Label(form_frame, text="Nome").grid(row=0, column=0, sticky="w")
        ttk.Entry(form_frame, textvariable=self.nome_var).grid(row=0, column=1, sticky="ew", padx=6)

        ttk.Label(form_frame, text="CPF").grid(row=1, column=0, sticky="w")
        ttk.Entry(form_frame, textvariable=self.cpf_var).grid(row=1, column=1, sticky="ew", padx=6)

        ttk.Label(form_frame, text="Tempo 300m (min)").grid(row=0, column=2, sticky="w")
        ttk.Entry(form_frame, textvariable=self.tempo300_var, width=10).grid(row=0, column=3, sticky="w", padx=6)

        ttk.Label(form_frame, text="Barra Fixa (rep)").grid(row=1, column=2, sticky="w")
        ttk.Entry(form_frame, textvariable=self.barra_var, width=10).grid(row=1, column=3, sticky="w", padx=6)

        ttk.Label(form_frame, text="Tempo 2.4km (min)").grid(row=0, column=4, sticky="w")
        ttk.Entry(form_frame, textvariable=self.tempo2400_var, width=10).grid(row=0, column=5, sticky="w", padx=6)

        btn_salvar = ttk.Button(form_frame, text="Salvar", command=self.on_save)
        btn_salvar.grid(row=1, column=4, columnspan=2, sticky="ew", padx=6)

        for col in [1, 3, 5]:
            form_frame.columnconfigure(col, weight=1)

        stats_frame = ttk.LabelFrame(self, text="Estatísticas")
        stats_frame.pack(fill="x")

        ttk.Label(stats_frame, text="Aptos:").grid(row=0, column=0, sticky="w")
        ttk.Label(stats_frame, textvariable=self.aprovados_var).grid(row=0, column=1, sticky="w", padx=(0, 12))

        ttk.Label(stats_frame, text="Inaptos:").grid(row=0, column=2, sticky="w")
        ttk.Label(stats_frame, textvariable=self.reprovados_var).grid(row=0, column=3, sticky="w", padx=(0, 12))

        btn_atualizar = ttk.Button(stats_frame, text="Atualizar Estatísticas", command=self.refresh_stats)
        btn_atualizar.grid(row=0, column=4, padx=6)

        btn_kmeans = ttk.Button(stats_frame, text="Mostrar gráfico K-Means", command=self.on_kmeans)
        btn_kmeans.grid(row=0, column=5, padx=6)

    def refresh_table(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
        candidates = self.controller.list_candidates()
        for c in candidates:
            self.tree.insert(
                "",
                "end",
                iid=str(c["_id"]),
                values=(
                    c.get("nome", ""),
                    c.get("cpf", ""),
                    c.get("tempo_300", ""),
                    c.get("barra_fixa", ""),
                    c.get("tempo_2400", ""),
                    c.get("status", ""),
                ),
            )

    def refresh_stats(self):
        stats = self.controller.get_status_counts()
        self.aprovados_var.set(str(stats.get("APROVADO", 0)))
        self.reprovados_var.set(str(stats.get("REPROVADO", 0)))

    def on_row_select(self, event=None):
        selection = self.tree.selection()
        if not selection:
            return
        candidate_id = selection[0]
        candidate = self.controller.get_candidate(candidate_id)
        if not candidate:
            return
        self.selected_candidate_id = candidate_id
        self.nome_var.set(candidate.get("nome", ""))
        self.cpf_var.set(candidate.get("cpf", ""))
        self.tempo300_var.set(str(candidate.get("tempo_300", "")))
        self.barra_var.set(str(candidate.get("barra_fixa", "")))
        self.tempo2400_var.set(str(candidate.get("tempo_2400", "")))

    def clear_form(self):
        self.selected_candidate_id = None
        self.nome_var.set("")
        self.cpf_var.set("")
        self.tempo300_var.set("")
        self.barra_var.set("")
        self.tempo2400_var.set("")
        self.tree.selection_remove(*self.tree.selection())

    def on_save(self):
        try:
            if self.selected_candidate_id is None:
                self.controller.create_candidate(
                    self.nome_var.get(),
                    self.cpf_var.get(),
                    self.tempo300_var.get(),
                    self.barra_var.get(),
                    self.tempo2400_var.get(),
                )
                messagebox.showinfo("Sucesso", "Candidato cadastrado")
            else:
                self.controller.update_candidate(
                    self.selected_candidate_id,
                    self.nome_var.get(),
                    self.cpf_var.get(),
                    self.tempo300_var.get(),
                    self.barra_var.get(),
                    self.tempo2400_var.get(),
                )
                messagebox.showinfo("Sucesso", "Candidato atualizado")

            self.refresh_table()
            self.refresh_stats()
            self.clear_form()
        except Exception as e:
            messagebox.showerror("Erro", str(e))

    def on_kmeans(self):
        try:
            self.controller.show_kmeans_graph()
        except Exception as e:
            messagebox.showerror("Erro", str(e))
