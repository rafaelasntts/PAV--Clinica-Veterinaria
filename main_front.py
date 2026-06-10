# FILE: main_front.py
import tkinter as tk
from tkinter import messagebox
from cliente_gui import ClinicaClienteApp
from exame_gui import ClinicaExameApp 
from animal_gui import ClinicaAnimalApp
from veterinario_gui import ClinicaVetApp
from consulta_gui import ClinicaConsultaApp

class MenuPrincipalApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Clínica Veterinária - Painel Principal")
        self.root.geometry("500x580") 
        self.root.configure(bg="#f5f6fa")
        self.root.resizable(False, False)

        self.setup_ui()

    def setup_ui(self):
        # ===== TITLE =====
        title = tk.Label(
            self.root,
            text="Menu Principal",
            font=("Segoe UI", 26, "bold"),
            bg="#f5f6fa",
            fg="#2d3436"
        )
        title.pack(pady=(30, 20))

        # ===== BUTTON FRAME =====
        button_frame = tk.Frame(self.root, bg="#f5f6fa")
        button_frame.pack()

        self.create_menu_button(button_frame, "Gerenciar Clientes", "#0984e3", self.abrir_clientes).pack(pady=8)
        self.create_menu_button(button_frame, "Gerenciar Animais", "#6c5ce7", self.abrir_animais).pack(pady=8)
        self.create_menu_button(button_frame, "Gerenciar Veterinários", "#e17055", self.abrir_vets).pack(pady=8)
        self.create_menu_button(button_frame, "Gerenciar Consultas", "#fdcb6e", self.abrir_consultas).pack(pady=8) 
        self.create_menu_button(button_frame, "Gerenciar Exames", "#20bf6b", self.abrir_exames).pack(pady=8)

    def create_menu_button(self, parent, text, color, command):
        button = tk.Button(
            parent, text=text, command=command, font=("Segoe UI", 13, "bold"),
            bg=color, fg="white", activebackground=color, activeforeground="white",
            relief="flat", cursor="hand2", width=25, height=2, bd=0
        )
        return button

    def abrir_clientes(self):
        nova_janela = tk.Toplevel(self.root)
        ClinicaClienteApp(nova_janela)

    def abrir_exames(self):
        nova_janela = tk.Toplevel(self.root)
        ClinicaExameApp(nova_janela)

    def abrir_animais(self):
        nova_janela = tk.Toplevel(self.root)
        ClinicaAnimalApp(nova_janela)

    def abrir_vets(self):
        nova_janela = tk.Toplevel(self.root)
        ClinicaVetApp(nova_janela)

    def abrir_consultas(self):
        nova_janela = tk.Toplevel(self.root)
        ClinicaConsultaApp(nova_janela)


if __name__ == "__main__":
    root = tk.Tk()
    app = MenuPrincipalApp(root)
    root.mainloop()