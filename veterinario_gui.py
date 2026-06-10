# FILE: veterinario_gui.py
import tkinter as tk
from tkinter import messagebox
import requests

API_URL = "http://127.0.0.1:8000/veterinarios"

class ClinicaVetApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Sistema Veterinário - Gestão de Veterinários")
        self.root.geometry("780x400")
        self.root.configure(bg="#f5f6fa")
        self.root.resizable(False, False)

        self.setup_ui()

    def setup_ui(self):
        title = tk.Label(self.root, text="Tela de Veterinários", font=("Segoe UI", 24, "bold"), bg="#f5f6fa", fg="#2d3436")
        title.pack(pady=(15, 10))

        form_frame = tk.Frame(self.root, bg="#f5f6fa")
        form_frame.pack(padx=40, fill="x")

        # ID VET
        lbl_id = tk.Label(form_frame, text="ID Vet:", font=("Segoe UI", 11, "bold"), bg="#f5f6fa", fg="#2d3436")
        lbl_id.grid(row=0, column=0, sticky="w", pady=5)
        id_container = tk.Frame(form_frame, bg="#f5f6fa")
        id_container.grid(row=0, column=1, padx=20, pady=5, sticky="w")
        self.entry_id = tk.Entry(id_container, font=("Segoe UI", 11), relief="solid", bd=1, width=15)
        self.entry_id.pack(side="left", ipady=4)

        # NOME
        lbl_nome = tk.Label(form_frame, text="Nome do Médico:", font=("Segoe UI", 11, "bold"), bg="#f5f6fa", fg="#2d3436")
        lbl_nome.grid(row=1, column=0, sticky="w", pady=5)
        self.entry_nome = tk.Entry(form_frame, font=("Segoe UI", 11), relief="solid", bd=1, width=45)
        self.entry_nome.grid(row=1, column=1, padx=20, pady=5, ipady=4)

        # CRMV
        lbl_crmv = tk.Label(form_frame, text="CRMV:", font=("Segoe UI", 11, "bold"), bg="#f5f6fa", fg="#2d3436")
        lbl_crmv.grid(row=2, column=0, sticky="w", pady=5)
        self.entry_crmv = tk.Entry(form_frame, font=("Segoe UI", 11), relief="solid", bd=1, width=45)
        self.entry_crmv.grid(row=2, column=1, padx=20, pady=5, ipady=4)

        # ESPECIALIDADE
        lbl_esp = tk.Label(form_frame, text="Especialidade:", font=("Segoe UI", 11, "bold"), bg="#f5f6fa", fg="#2d3436")
        lbl_esp.grid(row=3, column=0, sticky="w", pady=5)
        self.entry_especialidade = tk.Entry(form_frame, font=("Segoe UI", 11), relief="solid", bd=1, width=45)
        self.entry_especialidade.grid(row=3, column=1, padx=20, pady=5, ipady=4)

        # TELEFONE
        lbl_tel = tk.Label(form_frame, text="Telefone:", font=("Segoe UI", 11, "bold"), bg="#f5f6fa", fg="#2d3436")
        lbl_tel.grid(row=4, column=0, sticky="w", pady=5)
        self.entry_telefone = tk.Entry(form_frame, font=("Segoe UI", 11), relief="solid", bd=1, width=45)
        self.entry_telefone.grid(row=4, column=1, padx=20, pady=5, ipady=4)

        # BOTÕES
        button_frame = tk.Frame(self.root, bg="#f5f6fa")
        button_frame.pack(pady=15)

        self.create_button(button_frame, "Excluir", "#d63031", self.call_api_delete).grid(row=0, column=0, padx=5)
        self.create_button(button_frame, "Editar", "#e17055", self.call_api_put).grid(row=0, column=1, padx=5)
        self.create_button(button_frame, "Cadastrar", "#0984e3", self.call_api_post).grid(row=0, column=2, padx=5)
        self.create_button(button_frame, "Buscar ID", "#00cec9", self.call_api_get_by_id).grid(row=0, column=3, padx=5)
        self.create_button(button_frame, "Buscar All", "#6c5ce7", self.call_api_get_all).grid(row=0, column=4, padx=5)
        self.create_button(button_frame, "Limpar", "#636e72", self.clear_fields).grid(row=0, column=5, padx=5)

        # LISTA
        self.lbl_lista = tk.Label(self.root, text="Veterinários Cadastrados:", font=("Segoe UI", 11, "bold"), bg="#f5f6fa", fg="#2d3436")
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
        self.root.geometry("780x640")
        self.lbl_lista.pack(pady=(5, 2), padx=40, anchor="w")
        self.list_frame.pack(padx=40, fill="both", expand=True, pady=(0, 15))

    def esconder_lista_visual(self):
        self.lbl_lista.pack_forget()
        self.list_frame.pack_forget()
        self.root.geometry("780x400")

    def clear_fields(self):
        self.entry_id.delete(0, tk.END)
        self.entry_nome.delete(0, tk.END)
        self.entry_crmv.delete(0, tk.END)
        self.entry_especialidade.delete(0, tk.END)
        self.entry_telefone.delete(0, tk.END)
        self.esconder_lista_visual()

    def preencher_campos(self, vet):
        self.entry_id.delete(0, tk.END)
        self.entry_id.insert(0, vet.get("id_veterinario", ""))
        self.entry_nome.delete(0, tk.END)
        self.entry_nome.insert(0, vet.get("nome", ""))
        self.entry_crmv.delete(0, tk.END)
        self.entry_crmv.insert(0, vet.get("crmv", ""))
        self.entry_especialidade.delete(0, tk.END)
        self.entry_especialidade.insert(0, vet.get("especialidade", ""))
        self.entry_telefone.delete(0, tk.END)
        self.entry_telefone.insert(0, vet.get("telefone", ""))

    def on_select_item(self, event):
        widget = event.widget
        selection = widget.curselection()
        if selection:
            index = selection[0]
            texto = widget.get(index)
            try:
                id_vet = texto.split("|")[0].replace("ID:", "").strip()
                response = requests.get(API_URL)
                if response.status_code == 200:
                    for v in response.json():
                        if str(v.get("id_veterinario")) == id_vet:
                            self.preencher_campos(v)
                            break
            except Exception: pass

    def call_api_get_all(self):
        try:
            response = requests.get(API_URL)
            if response.status_code == 200:
                data = response.json()
                self.listbox.delete(0, tk.END)
                if data:
                    for v in data:
                        txt = f"ID: {v.get('id_veterinario'):<4} | Vet: {v.get('nome'):<20} | CRMV: {v.get('crmv'):<8} | Esp: {v.get('especialidade')}"
                        self.listbox.insert(tk.END, txt)
                    self.mostrar_lista_visual()
                    messagebox.showinfo("Sucesso", f"Foram encontrados {len(data)} veterinários.")
                else: messagebox.showwarning("Aviso", "Nenhum veterinário cadastrado.")
        except Exception as e: messagebox.showerror("Erro", str(e))

    def call_api_get_by_id(self):
        id_v = self.entry_id.get().strip()
        if not id_v: return messagebox.showwarning("Aviso", "Informe um ID.")
        try:
            response = requests.get(API_URL)
            if response.status_code == 200:
                for v in response.json():
                    if str(v.get("id_veterinario")) == id_v:
                        self.preencher_campos(v)
                        return messagebox.showinfo("Sucesso", "Veterinário carregado!")
                messagebox.showwarning("Erro", "Não encontrado.")
        except Exception as e: messagebox.showerror("Erro", str(e))

    def call_api_post(self):
        nome = self.entry_nome.get().strip()
        crmv = self.entry_crmv.get().strip() 

       
        if not nome:
            return messagebox.showwarning(
                "Erro de Validação", 
                "O campo Nome do Veterinário é obrigatório e não pode ficar em branco!"
            )

       
        if not crmv:
            return messagebox.showwarning(
                "Erro de Validação", 
                "Requisito 8: O registo do CRMV é obrigatório para efetuar o cadastro do veterinário!"
            )
        try:
            data = {
                "nome": nome,
                "crmv": crmv,
                "especialidade": self.entry_especialidade.get(),
                "telefone": self.entry_telefone.get()
            }
            res = requests.post(API_URL, json=data)
            if res.status_code in [200, 201]:
                messagebox.showinfo("Sucesso", "Veterinário cadastrado!")
                self.clear_fields()
            else: messagebox.showerror("Erro", res.text)
        except Exception as e: messagebox.showerror("Erro", str(e))

    def call_api_put(self):
        id_v = self.entry_id.get()
        if not id_v: return messagebox.showwarning("Aviso", "Informe o ID.")

        nome = self.entry_nome.get().strip()
        crmv = self.entry_crmv.get().strip()

        
        if not nome:
            return messagebox.showwarning("Erro de Validação", "O campo Nome não pode ficar vazio na edição!")

        
        if not crmv:
            return messagebox.showwarning("Erro de Validação", "Requisito do Sistema: Não é permitido atualizar deixando o CRMV em branco!")
        try:
            data = {
                "nome": nome,
                "crmv": crmv,
                "especialidade": self.entry_especialidade.get(),
                "telefone": self.entry_telefone.get()
            }
            res = requests.put(f"{API_URL}/{id_v}", json=data)
            if res.status_code in [200, 201]:
                messagebox.showinfo("Sucesso", "Veterinário atualizado!")
                self.clear_fields()
            else: messagebox.showerror("Erro", res.text)
        except Exception as e: messagebox.showerror("Erro", str(e))

    def call_api_delete(self):
        id_v = self.entry_id.get()
        if not id_v: return messagebox.showwarning("Aviso", "Informe o ID.")
        try:
            res = requests.delete(f"{API_URL}/{id_v}")
            if res.status_code == 200:
                messagebox.showinfo("Sucesso", "Veterinário removido!")
                self.clear_fields()
            else: messagebox.showerror("Erro", res.text)
        except Exception as e: messagebox.showerror("Erro", str(e))

if __name__ == "__main__":
    root = tk.Tk()
    app = ClinicaVetApp(root)
    root.mainloop()