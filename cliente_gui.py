import tkinter as tk
from tkinter import messagebox
import requests

API_URL = "http://127.0.0.1:8000/clientes"

class ClinicaClienteApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Sistema Veterinário - Gestão de Clientes")
        self.root.geometry("780x440") 
        self.root.configure(bg="#f5f6fa")
        self.root.resizable(False, False)

        self.setup_ui()

    def setup_ui(self):
        # ===== TITLE =====
        title = tk.Label(
            self.root, text="Tela de Cliente", font=("Segoe UI", 24, "bold"),
            bg="#f5f6fa", fg="#2d3436"
        )
        title.pack(pady=(15, 10))

        # ===== FORM FRAME =====
        form_frame = tk.Frame(self.root, bg="#f5f6fa")
        form_frame.pack(padx=40, fill="x")

        # ===== ID_CLIENTE =====
        lbl_id = tk.Label(form_frame, text="ID Cliente:", font=("Segoe UI", 11, "bold"), bg="#f5f6fa", fg="#2d3436")
        lbl_id.grid(row=0, column=0, sticky="w", pady=5)
        
        id_container = tk.Frame(form_frame, bg="#f5f6fa")
        id_container.grid(row=0, column=1, padx=20, pady=5, sticky="w")
        
        self.entry_id = tk.Entry(id_container, font=("Segoe UI", 11), relief="solid", bd=1, width=15)
        self.entry_id.pack(side="left", ipady=4)
        
        lbl_id_hint = tk.Label(id_container, text="*(Use apenas para Buscar, Editar ou Deletar)*", font=("Segoe UI", 9, "italic"), bg="#f5f6fa", fg="#7f8c8d")
        lbl_id_hint.pack(side="left", padx=10)

        # ===== NOME =====
        lbl_nome = tk.Label(form_frame, text="Nome:", font=("Segoe UI", 11, "bold"), bg="#f5f6fa", fg="#2d3436")
        lbl_nome.grid(row=1, column=0, sticky="w", pady=5)
        self.entry_nome = tk.Entry(form_frame, font=("Segoe UI", 11), relief="solid", bd=1, width=45)
        self.entry_nome.grid(row=1, column=1, padx=20, pady=5, ipady=4)

        # ===== CPF =====
        lbl_cpf = tk.Label(form_frame, text="CPF:", font=("Segoe UI", 11, "bold"), bg="#f5f6fa", fg="#2d3436")
        lbl_cpf.grid(row=2, column=0, sticky="w", pady=5)
        self.entry_cpf = tk.Entry(form_frame, font=("Segoe UI", 11), relief="solid", bd=1, width=45)
        self.entry_cpf.grid(row=2, column=1, padx=20, pady=5, ipady=4)

        # ===== TELEFONE =====
        lbl_telefone = tk.Label(form_frame, text="Telefone:", font=("Segoe UI", 11, "bold"), bg="#f5f6fa", fg="#2d3436")
        lbl_telefone.grid(row=3, column=0, sticky="w", pady=5)
        self.entry_telefone = tk.Entry(form_frame, font=("Segoe UI", 11), relief="solid", bd=1, width=45)
        self.entry_telefone.grid(row=3, column=1, padx=20, pady=5, ipady=4)

        # ===== ENDEREÇO =====
        lbl_endereco = tk.Label(form_frame, text="Endereço:", font=("Segoe UI", 11, "bold"), bg="#f5f6fa", fg="#2d3436")
        lbl_endereco.grid(row=4, column=0, sticky="w", pady=5)
        self.entry_endereco = tk.Entry(form_frame, font=("Segoe UI", 11), relief="solid", bd=1, width=45)
        self.entry_endereco.grid(row=4, column=1, padx=20, pady=5, ipady=4)

        # ===== EMAIL =====
        lbl_email = tk.Label(form_frame, text="Email:", font=("Segoe UI", 11, "bold"), bg="#f5f6fa", fg="#2d3436")
        lbl_email.grid(row=5, column=0, sticky="w", pady=5)
        self.entry_email = tk.Entry(form_frame, font=("Segoe UI", 11), relief="solid", bd=1, width=45)
        self.entry_email.grid(row=5, column=1, padx=20, pady=5, ipady=4)

        # ===== BUTTON FRAME =====
        button_frame = tk.Frame(self.root, bg="#f5f6fa")
        button_frame.pack(pady=15)

        self.create_button(button_frame, "Excluir", "#d63031", self.call_api_delete).grid(row=0, column=0, padx=5)
        self.create_button(button_frame, "Editar", "#e17055", self.call_api_put).grid(row=0, column=1, padx=5)
        self.create_button(button_frame, "Cadastrar", "#0984e3", self.call_api_post).grid(row=0, column=2, padx=5)
        self.create_button(button_frame, "Buscar ID", "#00cec9", self.call_api_get_by_id).grid(row=0, column=3, padx=5)
        self.create_button(button_frame, "Buscar All", "#6c5ce7", self.call_api_get_all).grid(row=0, column=4, padx=5)
        self.create_button(button_frame, "Limpar", "#636e72", self.clear_fields).grid(row=0, column=5, padx=5)

        self.lbl_lista = tk.Label(self.root, text="Clientes Cadastrados no Banco de Dados:", font=("Segoe UI", 11, "bold"), bg="#f5f6fa", fg="#2d3436")
        
        self.list_frame = tk.Frame(self.root, bg="#f5f6fa")
        self.scrollbar = tk.Scrollbar(self.list_frame, orient="vertical")
        self.scrollbar.pack(side="right", fill="y")
        
        self.listbox_clientes = tk.Listbox(self.list_frame, font=("Consolas", 11), relief="solid", bd=1, yscrollcommand=self.scrollbar.set)
        self.listbox_clientes.pack(side="left", fill="both", expand=True)
        self.scrollbar.config(command=self.listbox_clientes.yview)
        
        self.listbox_clientes.bind("<<ListboxSelect>>", self.on_select_item)

    def create_button(self, parent, text, color, command):
        return tk.Button(
            parent, text=text, command=command, font=("Segoe UI", 10, "bold"),
            bg=color, fg="white", activebackground=color, activeforeground="white",
            relief="flat", cursor="hand2", width=10, height=2, bd=0
        )

    def mostrar_lista_visual(self):
        """Aumenta a tela e faz a lista aparecer"""
        self.root.geometry("780x680") # Estica a janela para baixo
        self.lbl_lista.pack(pady=(5, 2), padx=40, anchor="w")
        self.list_frame.pack(padx=40, fill="both", expand=True, pady=(0, 15))

    def esconder_lista_visual(self):
        """Encolhe a tela e esconde a lista completamente"""
        self.lbl_lista.pack_forget()
        self.list_frame.pack_forget()
        self.root.geometry("780x440") # Volta ao tamanho compacto original

    def clear_fields(self):
        self.entry_id.delete(0, tk.END)
        self.entry_nome.delete(0, tk.END)
        self.entry_cpf.delete(0, tk.END)
        self.entry_telefone.delete(0, tk.END)
        self.entry_endereco.delete(0, tk.END)
        self.entry_email.delete(0, tk.END)
        self.esconder_lista_visual() 

    def preencher_campos(self, cliente):
        self.entry_id.delete(0, tk.END)
        self.entry_id.insert(0, cliente.get("id_cliente", ""))
        self.entry_nome.delete(0, tk.END)
        self.entry_nome.insert(0, cliente.get("nome", ""))
        self.entry_cpf.delete(0, tk.END)
        self.entry_cpf.insert(0, cliente.get("cpf", ""))
        self.entry_telefone.delete(0, tk.END)
        self.entry_telefone.insert(0, cliente.get("telefone", ""))
        self.entry_endereco.delete(0, tk.END)
        self.entry_endereco.insert(0, cliente.get("endereco", ""))
        self.entry_email.delete(0, tk.END)
        self.entry_email.insert(0, cliente.get("email", ""))

    def on_select_item(self, event):
        widget = event.widget
        selection = widget.curselection()
        if selection:
            index = selection[0]
            texto_selecionado = widget.get(index)
            try:
                id_cliente = texto_selecionado.split("|")[0].replace("ID:", "").strip()
                response = requests.get(API_URL)
                if response.status_code == 200:
                    for c in response.json():
                        if str(c.get("id_cliente")) == id_cliente:
                            self.preencher_campos(c)
                            break
            except Exception:
                pass

    def call_api_get_all(self):
        try:
            response = requests.get(API_URL)
            if response.status_code == 200:
                data = response.json()
                self.listbox_clientes.delete(0, tk.END)
                
                if data:
                    for c in data:
                        item_texto = f"ID: {c.get('id_cliente'):<4} | Nome: {c.get('nome'):<25} | CPF: {c.get('cpf')}"
                        self.listbox_clientes.insert(tk.END, item_texto)
                    
                    self.mostrar_lista_visual() # ✨ SURGE A LISTA AQUI!
                    messagebox.showinfo("Sucesso", f"Foram encontrados {len(data)} clientes.")
                else:
                    messagebox.showwarning("Aviso", "Nenhum cliente cadastrado no banco.")
            else:
                messagebox.showerror("Erro", "Erro ao buscar dados.")
        except Exception as e:
            messagebox.showerror("Erro", str(e))

    def call_api_get_by_id(self):
        id_cliente = self.entry_id.get().strip()
        if not id_cliente:
            messagebox.showwarning("Aviso", "Informe um ID no campo correspondente para buscar.")
            return
        try:
            response = requests.get(API_URL)
            if response.status_code == 200:
                data = response.json()
                encontrado = False
                for c in data:
                    if str(c.get("id_cliente")) == id_cliente:
                        self.preencher_campos(c)
                        encontrado = True
                        messagebox.showinfo("Sucesso", f"Cliente ID {id_cliente} carregado!")
                        break
                if not encontrado:
                    messagebox.showwarning("Não encontrado", f"Nenhum cliente com o ID {id_cliente} foi localizado.")
            else:
                messagebox.showerror("Erro", "Erro ao acessar o servidor.")
        except Exception as e:
            messagebox.showerror("Erro", str(e))

    def call_api_post(self):
        nome = self.entry_nome.get().strip()
        telefone = self.entry_telefone.get().strip()
        email = self.entry_email.get().strip()

        if not nome:
            return messagebox.showwarning("Erro de Validação", "Requisito do Sistema: O campo Nome é obrigatório!")

        if not telefone and not email:
            return messagebox.showwarning(
                "Erro de Validação", 
                "Requisito do Sistema: O cliente deve possuir pelo menos um meio de contato válido (Telefone ou Email)!"
            )

        try:
            data = {
                "nome": self.entry_nome.get(),
                "cpf": self.entry_cpf.get(),
                "telefone": self.entry_telefone.get(),
                "endereco": self.entry_endereco.get(),
                "email": self.entry_email.get(),
            }
            response = requests.post(API_URL, json=data)

            if response.status_code in [200, 201]:
                res_json = response.json()
                messagebox.showinfo("Sucesso", res_json.get("mensagem", "Cliente cadastrado!"))
                self.clear_fields()
            else:
                erro_detalhe = response.json().get("detail", response.text)
                messagebox.showerror("Erro de Validação", erro_detalhe)
        except Exception as e:
            messagebox.showerror("Erro", str(e))

    def call_api_put(self):
        telefone = self.entry_telefone.get().strip()
        email = self.entry_email.get().strip()
        nome = self.entry_nome.get().strip()

        if not nome:
            return messagebox.showwarning("Erro de Validação", "Requisito do Sistema: O campo Nome é obrigatório!")

        if not telefone and not email:
            return messagebox.showwarning(
                "Erro de Validação", 
                "Requisito do Sistema: Não é permitido atualizar o cliente deixando Telefone e Email vazios!"
            )

        try:
            id_cliente = self.entry_id.get()
            if not id_cliente:
                messagebox.showwarning("Aviso", "Informe o ID do cliente para editar")
                return

            data = {
                "nome": self.entry_nome.get(),
                "cpf": self.entry_cpf.get(),
                "telefone": self.entry_telefone.get(),
                "endereco": self.entry_endereco.get(),
                "email": self.entry_email.get(),
            }
            response = requests.put(f"{API_URL}/{id_cliente}", json=data)

            if response.status_code in [200, 201]:
                messagebox.showinfo("Sucesso", "Cliente atualizado com sucesso")
                self.clear_fields()
            else:
                erro_detalhe = response.json().get("detail", response.text)
                messagebox.showerror("Erro", erro_detalhe)
        except Exception as e:
            messagebox.showerror("Erro", str(e))

    def call_api_delete(self):
        id_cliente = self.entry_id.get()
        if not id_cliente:
            messagebox.showwarning("Aviso", "Informe o ID do cliente")
            return

        try:
            response = requests.delete(f"{API_URL}/{id_cliente}")
            if response.status_code == 200:
                messagebox.showinfo("Sucesso", "Cliente removido com sucesso")
                self.clear_fields()
            else:
                erro_detalhe = response.json().get("detail", response.text)
                messagebox.showerror("Erro", erro_detalhe)
        except Exception as e:
            messagebox.showerror("Erro", str(e))


if __name__ == "__main__":
    root = tk.Tk()
    app = ClinicaClienteApp(root)
    root.mainloop()