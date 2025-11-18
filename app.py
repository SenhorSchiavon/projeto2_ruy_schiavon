import tkinter as tk
from tkinter import ttk
from dotenv import load_dotenv
from database import get_database
from models.candidate_model import CandidateModel
from controllers.candidate_controller import CandidateController
from views.main_view import MainView

def main():
    load_dotenv()
    db = get_database()
    model = CandidateModel(db)
    controller = CandidateController(model)

    root = tk.Tk()
    root.title("Teste Físico - K-Means")
    root.geometry("1000x600")
    style = ttk.Style(root)
    try:
        style.theme_use("clam")
    except Exception:
        pass
    MainView(root, controller)
    root.mainloop()

if __name__ == "__main__":
    main()
