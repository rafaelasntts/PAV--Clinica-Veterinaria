import tkinter as tk
from tkinter import messagebox
import requests

API_URL = "http://127.0.0.1:8000/animais"

class ClinicaAnimalApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Sistema Veterinário - Gestão de Animais")
        self.root.geometry("780x460") 
        self.root.configure(bg="#f5f6fa")
        self.root.resizable(False, False)

        self.setup_ui()

    def setup_ui(self):
        title = tk.Label(self.root, text="Tela de Animais", font=("Segoe UI", 24, "bold"), bg="#f5f6fa", fg="#2d3436")
        title.pack(pady=(15, 10))

        form_frame = tk.Frame(self.root, bg="#f5f6fa")
        form_frame.pack(padx=40, fill="x")

        # ID ANIMAL
        lbl_id = tk.Label(form_frame, text="ID Animal:", font=("Segoe UI", 11, "bold"), bg="#f5f6fa", fg="#2d3436")
        lbl_id.grid(row=0, column=0, sticky="w", pady=5)
        id_container = tk.Frame(form_frame, bg="#f5f6fa")
        id_container.grid(row=0, column=1, padx=20, pady=5, sticky="w")
        self.entry_id = tk.Entry(id_container, font=("Segoe UI", 11), relief="solid", bd=1, width=15)
        self.entry_id.pack(side="left", ipady=4)
        lbl_id_hint = tk.Label(id_container, text="*(Buscar, Editar ou Deletar)*", font=("Segoe UI", 9, "italic"), bg="#f5f6fa", fg="#7f8c8d")
        lbl_id_hint.pack(side="left", padx=10)

        # NOME
        lbl_nome = tk.Label(form_frame, text="Nome do Pet:", font=("Segoe UI", 11, "bold"), bg="#f5f6fa", fg="#2d3436")
        lbl_nome.grid(row=1, column=0, sticky="w", pady=5)
        self.entry_nome = tk.Entry(form_frame, font=("Segoe UI", 11), relief="solid", bd=1, width=45)
        self.entry_nome.grid(row=1, column=1, padx=20, pady=5, ipady=4)

        # ESPECIE
        lbl_especie = tk.Label(form_frame, text="Espécie:", font=("Segoe UI", 11, "bold"), bg="#f5f6fa", fg="#2d3436")
        lbl_especie.grid(row=2, column=0, sticky="w", pady=5)
        self.entry_especie = tk.Entry(form_frame, font=("Segoe UI", 11), relief="solid", bd=1, width=45)
        self.entry_especie.grid(row=2, column=1, padx=20, pady=5, ipady=4)

        # RAÇA
        lbl_raca = tk.Label(form_frame, text="Raça:", font=("Segoe UI", 11, "bold"), bg="#f5f6fa", fg="#2d3436")
        lbl_raca.grid(row=3, column=0, sticky="w", pady=5)
        self.entry_raca = tk.Entry(form_frame, font=("Segoe UI", 11), relief="solid", bd=1, width=45)
        self.entry_raca.grid(row=3, column=1, padx=20, pady=5, ipady=4)

        # ✨ NOVO CAMPO: SEXO ✨
        lbl_sexo = tk.Label(form_frame, text="Sexo:", font=("Segoe UI", 11, "bold"), bg="#f5f6fa", fg="#2d3436")
        lbl_sexo.grid(row=4, column=0, sticky="w", pady=5)
        self.entry_sexo = tk.Entry(form_frame, font=("Segoe UI", 11), relief="solid", bd=1, width=45)
        self.entry_sexo.grid(row=4, column=1, padx=20, pady=5, ipady=4)

        # IDADE
        lbl_idade = tk.Label(form_frame, text="Idade:", font=("Segoe UI", 11, "bold"), bg="#f5f6fa", fg="#2d3436")
        lbl_idade.grid(row=5, column=0, sticky="w", pady=5)
        self.entry_idade = tk.Entry(form_frame, font=("Segoe UI", 11), relief="solid", bd=1, width=45)
        self.entry_idade.grid(row=5, column=1, padx=20, pady=5, ipady=4)

        # ID_CLIENTE (Dono)
        lbl_cliente = tk.Label(form_frame, text="ID do Dono:", font=("Segoe UI", 11, "bold"), bg="#f5f6fa", fg="#2d3436")
        lbl_cliente.grid(row=6, column=0, sticky="w", pady=5)
        self.entry_cliente = tk.Entry(form_frame, font=("Segoe UI", 11), relief="solid", bd=1, width=45)
        self.entry_cliente.grid(row=6, column=1, padx=20, pady=5, ipady=4)

        # BOTÕES
        button_frame = tk.Frame(self.root, bg="#f5f6fa")
        button_frame.pack(pady=15)

        self.create_button(button_frame, "Excluir", "#d63031", self.call_api_delete).grid(row=0, column=0, padx=5)
        self.create_button(button_frame, "Editar", "#e17055", self.call_api_put).grid(row=0, column=1, padx=5)
        self.create_button(button_frame, "Cadastrar", "#0984e3", self.call_api_post).grid(row=0, column=2, padx=5)
        self.create_button(button_frame, "Buscar ID", "#00cec9", self.call_api_get_by_id).grid(row=0, column=3, padx=5)
        self.create_button(button_frame, "Buscar All", "#6c5ce7", self.call_api_get_all).grid(row=0, column=4, padx=5)
        self.create_button(button_frame, "Limpar", "#636e72", self.clear_fields).grid(row=0, column=5, padx=5)

        # LISTA DINÂMICA
        self.lbl_lista = tk.Label(self.root, text="Animais Cadastrados:", font=("Segoe UI", 11, "bold"), bg="#f5f6fa", fg="#2d3436")
        self.list_frame = tk.Frame(self.root, bg="#f5f6fa")
        self.scrollbar = tk.Scrollbar(self.list_frame, orient="vertical")
        self.scrollbar.pack(side="right", fill="y")
        self.listbox = tk.Listbox(self.list_frame, font=("Consolas", 11), relief="solid", bd=1, yscrollcommand=self.scrollbar.set)
        self.listbox.pack(side="left", fill="both", expand=True)
        self.scrollbar.config(command=self.listbox.yview)
        self.listbox.bind("<<ListboxSelect>>", self.on_select_item)

    def create_button(self, parent, text, color, command):
        return tk.Button(parent, text=text, command=command, font=("Segoe UI", 10, "bold"), bg=color, fg="white", activebackground=color, relief="flat", cursor="hand2", width=10, height=2, bd=0)

    def mostrar_lista_visual(self):
        self.root.geometry("780x690") 
        self.lbl_lista.pack(pady=(5, 2), padx=40, anchor="w")
        self.list_frame.pack(padx=40, fill="both", expand=True, pady=(0, 15))

    def esconder_lista_visual(self):
        self.lbl_lista.pack_forget()
        self.list_frame.pack_forget()
        self.root.geometry("780x460")

    def clear_fields(self):
        self.entry_id.delete(0, tk.END)
        self.entry_nome.delete(0, tk.END)
        self.entry_especie.delete(0, tk.END)
        self.entry_raca.delete(0, tk.END)
        self.entry_sexo.delete(0, tk.END) 
        self.entry_idade.delete(0, tk.END)
        self.entry_cliente.delete(0, tk.END)
        self.esconder_lista_visual()

    def preencher_campos(self, animal):
        self.entry_id.delete(0, tk.END)
        self.entry_id.insert(0, animal.get("id_animal", ""))
        self.entry_nome.delete(0, tk.END)
        self.entry_nome.insert(0, animal.get("nome", ""))
        self.entry_especie.delete(0, tk.END)
        self.entry_especie.insert(0, animal.get("especie", ""))
        self.entry_raca.delete(0, tk.END)
        self.entry_raca.insert(0, animal.get("raca", ""))
        self.entry_sexo.delete(0, tk.END)
        self.entry_sexo.insert(0, animal.get("sexo", "")) 
        self.entry_idade.delete(0, tk.END)
        self.entry_idade.insert(0, animal.get("idade", ""))
        self.entry_cliente.delete(0, tk.END)
        self.entry_cliente.insert(0, animal.get("id_cliente", ""))

    def on_select_item(self, event):
        widget = event.widget
        selection = widget.curselection()
        if selection:
            index = selection[0]
            texto = widget.get(index)
            try:
                id_animal = texto.split("|")[0].replace("ID:", "").strip()
                response = requests.get(API_URL)
                if response.status_code == 200:
                    for a in response.json():
                        if str(a.get("id_animal")) == id_animal:
                            self.preencher_campos(a)
                            break
            except Exception: pass

    def call_api_get_all(self):
        try:
            response = requests.get(API_URL)
            if response.status_code == 200:
                data = response.json()
                self.listbox.delete(0, tk.END)
                if data:
                    for a in data:
                        txt = f"ID: {a.get('id_animal'):<4} | Pet: {a.get('nome'):<12} | Sexo: {a.get('sexo'):<6} | Espécie: {a.get('especie'):<10} | Dono ID: {a.get('id_cliente')}"
                        self.listbox.insert(tk.END, txt)
                    self.mostrar_lista_visual()
                    messagebox.showinfo("Sucesso", f"Foram encontrados {len(data)} animais.")
                else: messagebox.showwarning("Aviso", "Nenhum animal cadastrado.")
        except Exception as e: messagebox.showerror("Erro", str(e))

    def call_api_get_by_id(self):
        id_an = self.entry_id.get().strip()
        if not id_an: return messagebox.showwarning("Aviso", "Informe um ID.")
        try:
            response = requests.get(API_URL)
            if response.status_code == 200:
                for a in response.json():
                    if str(a.get("id_animal")) == id_an:
                        self.preencher_campos(a)
                        return messagebox.showinfo("Sucesso", "Animal carregado!")
                messagebox.showwarning("Erro", "Não encontrado.")
        except Exception as e: messagebox.showerror("Erro", str(e))

    def call_api_post(self):
        try:
            data = {
                "nome": self.entry_nome.get(),
                "especie": self.entry_especie.get(),
                "raca": self.entry_raca.get(),
                "sexo": self.entry_sexo.get(), 
                "idade": int(self.entry_idade.get() or 0),
                "id_cliente": int(self.entry_cliente.get() or 0)
            }
            res = requests.post(API_URL, json=data)
            if res.status_code in [200, 201]:
                messagebox.showinfo("Sucesso", "Animal cadastrado!")
                self.clear_fields()
            else: messagebox.showerror("Erro", res.text)
        except Exception as e: messagebox.showerror("Erro", str(e))

    def call_api_put(self):
        id_an = self.entry_id.get()
        if not id_an: return messagebox.showwarning("Aviso", "Informe o ID.")
        try:
            data = {
                "nome": self.entry_nome.get(),
                "especie": self.entry_especie.get(),
                "raca": self.entry_raca.get(),
                "sexo": self.entry_sexo.get(), 
                "idade": int(self.entry_idade.get() or 0),
                "id_cliente": int(self.entry_cliente.get() or 0)
            }
            res = requests.put(f"{API_URL}/{id_an}", json=data)
            if res.status_code in [200, 201]:
                messagebox.showinfo("Sucesso", "Animal updated!")
                self.clear_fields()
            else: messagebox.showerror("Erro", res.text)
        except Exception as e: messagebox.showerror("Erro", str(e))

    def call_api_delete(self):
        id_an = self.entry_id.get()
        if not id_an: return messagebox.showwarning("Aviso", "Informe o ID.")
        try:
            res = requests.delete(f"{API_URL}/{id_an}")
            if res.status_code == 200:
                messagebox.showinfo("Sucesso", "Animal removido!")
                self.clear_fields()
            else: messagebox.showerror("Erro", res.text)
        except Exception as e: messagebox.showerror("Erro", str(e))

if __name__ == "__main__":
    root = tk.Tk()
    app = ClinicaAnimalApp(root)
    root.mainloop()