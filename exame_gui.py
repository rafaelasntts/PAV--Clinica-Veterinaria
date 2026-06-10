import tkinter as tk
from tkinter import messagebox
import requests

API_URL = "http://127.0.0.1:8000/exames"

class ClinicaExameApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Sistema Veterinário - Gestão de Exames")
        self.root.geometry("780x400")
        self.root.configure(bg="#f5f6fa")
        self.root.resizable(False, False)

        self.setup_ui()

    def setup_ui(self):
        # ===== TITLE =====
        title = tk.Label(
            self.root, text="Tela de Exame", font=("Segoe UI", 24, "bold"),
            bg="#f5f6fa", fg="#2d3436"
        )
        title.pack(pady=(15, 10))

        # ===== FORM FRAME =====
        form_frame = tk.Frame(self.root, bg="#f5f6fa")
        form_frame.pack(padx=40, fill="x")

        # ===== ID_EXAME =====
        lbl_id = tk.Label(form_frame, text="ID Exame:", font=("Segoe UI", 11, "bold"), bg="#f5f6fa", fg="#2d3436")
        lbl_id.grid(row=0, column=0, sticky="w", pady=5)
        
        id_container = tk.Frame(form_frame, bg="#f5f6fa")
        id_container.grid(row=0, column=1, padx=20, pady=5, sticky="w")
        
        self.entry_id = tk.Entry(id_container, font=("Segoe UI", 11), relief="solid", bd=1, width=15)
        self.entry_id.pack(side="left", ipady=4)
        
        lbl_id_hint = tk.Label(id_container, text="*(Use apenas para Buscar, Editar ou Deletar)*", font=("Segoe UI", 9, "italic"), bg="#f5f6fa", fg="#7f8c8d")
        lbl_id_hint.pack(side="left", padx=10)

        # ===== NOME DO EXAME =====
        lbl_nome = tk.Label(form_frame, text="Nome do Exame:", font=("Segoe UI", 11, "bold"), bg="#f5f6fa", fg="#2d3436")
        lbl_nome.grid(row=1, column=0, sticky="w", pady=5)
        self.entry_nome = tk.Entry(form_frame, font=("Segoe UI", 11), relief="solid", bd=1, width=45)
        self.entry_nome.grid(row=1, column=1, padx=20, pady=5, ipady=4)

        # ===== DESCRIÇÃO =====
        lbl_descricao = tk.Label(form_frame, text="Descrição:", font=("Segoe UI", 11, "bold"), bg="#f5f6fa", fg="#2d3436")
        lbl_descricao.grid(row=2, column=0, sticky="w", pady=5)
        self.entry_descricao = tk.Entry(form_frame, font=("Segoe UI", 11), relief="solid", bd=1, width=45)
        self.entry_descricao.grid(row=2, column=1, padx=20, pady=5, ipady=4)

        # ===== VALOR (REQUISITO FINANCEIRO) =====
        lbl_valor = tk.Label(form_frame, text="Valor (R$):", font=("Segoe UI", 11, "bold"), bg="#f5f6fa", fg="#2d3436")
        lbl_valor.grid(row=3, column=0, sticky="w", pady=5)
        self.entry_valor = tk.Entry(form_frame, font=("Segoe UI", 11), relief="solid", bd=1, width=45)
        self.entry_valor.grid(row=3, column=1, padx=20, pady=5, ipady=4)

        # ===== ID_CONSULTA (CHAVE ESTRANGEIRA) =====
        lbl_consulta = tk.Label(form_frame, text="ID Consulta:", font=("Segoe UI", 11, "bold"), bg="#f5f6fa", fg="#2d3436")
        lbl_consulta.grid(row=4, column=0, sticky="w", pady=5)
        self.entry_consulta = tk.Entry(form_frame, font=("Segoe UI", 11), relief="solid", bd=1, width=45)
        self.entry_consulta.grid(row=4, column=1, padx=20, pady=5, ipady=4)

        # ===== BUTTON FRAME =====
        button_frame = tk.Frame(self.root, bg="#f5f6fa")
        button_frame.pack(pady=15)

        self.create_button(button_frame, "Excluir", "#d63031", self.call_api_delete).grid(row=0, column=0, padx=5)
        self.create_button(button_frame, "Editar", "#e17055", self.call_api_put).grid(row=0, column=1, padx=5)
        self.create_button(button_frame, "Cadastrar", "#0984e3", self.call_api_post).grid(row=0, column=2, padx=5)
        self.create_button(button_frame, "Buscar ID", "#00cec9", self.call_api_get_by_id).grid(row=0, column=3, padx=5)
        self.create_button(button_frame, "Buscar All", "#6c5ce7", self.call_api_get_all).grid(row=0, column=4, padx=5)
        self.create_button(button_frame, "Limpar", "#636e72", self.clear_fields).grid(row=0, column=5, padx=5)

        # ===== COMPONENTES DA LISTA (Ocultos inicialmente) =====
        self.lbl_lista = tk.Label(self.root, text="Exames Cadastrados no Banco de Dados:", font=("Segoe UI", 11, "bold"), bg="#f5f6fa", fg="#2d3436")
        
        self.list_frame = tk.Frame(self.root, bg="#f5f6fa")
        self.scrollbar = tk.Scrollbar(self.list_frame, orient="vertical")
        self.scrollbar.pack(side="right", fill="y")
        
        self.listbox_exames = tk.Listbox(self.list_frame, font=("Consolas", 11), relief="solid", bd=1, yscrollcommand=self.scrollbar.set)
        self.listbox_exames.pack(side="left", fill="both", expand=True)
        self.scrollbar.config(command=self.listbox_exames.yview)
        
        self.listbox_exames.bind("<<ListboxSelect>>", self.on_select_item)

    def create_button(self, parent, text, color, command):
        return tk.Button(
            parent, text=text, command=command, font=("Segoe UI", 10, "bold"),
            bg=color, fg="white", activebackground=color, activeforeground="white",
            relief="flat", cursor="hand2", width=10, height=2, bd=0
        )

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
        self.entry_descricao.delete(0, tk.END)
        self.entry_valor.delete(0, tk.END)
        self.entry_consulta.delete(0, tk.END)
        self.esconder_lista_visual()

    def preencher_campos(self, exame):
        self.entry_id.delete(0, tk.END)
        self.entry_id.insert(0, exame.get("id_exame", ""))
        self.entry_nome.delete(0, tk.END)
        self.entry_nome.insert(0, exame.get("nome", ""))
        self.entry_descricao.delete(0, tk.END)
        self.entry_descricao.insert(0, exame.get("descricao", ""))
        self.entry_valor.delete(0, tk.END)
        self.entry_valor.insert(0, exame.get("valor", ""))
        self.entry_consulta.delete(0, tk.END)
        self.entry_consulta.insert(0, exame.get("id_consulta", ""))

    def on_select_item(self, event):
        widget = event.widget
        selection = widget.curselection()
        if selection:
            index = selection[0]
            texto_selecionado = widget.get(index)
            try:
                id_exame = texto_selecionado.split("|")[0].replace("ID:", "").strip()
                response = requests.get(API_URL)
                if response.status_code == 200:
                    for e in response.json():
                        if str(e.get("id_exame")) == id_exame:
                            self.preencher_campos(e)
                            break
            except Exception:
                pass

    def call_api_get_all(self):
        try:
            response = requests.get(API_URL)
            if response.status_code == 200:
                data = response.json()
                self.listbox_exames.delete(0, tk.END)
                
                if data:
                    for e in data:
                        item_texto = f"ID: {e.get('id_exame'):<4} | Exame: {e.get('nome'):<20} | R$: {e.get('valor'):<8} | Consulta: {e.get('id_consulta')}"
                        self.listbox_exames.insert(tk.END, item_texto)
                    
                    self.mostrar_lista_visual() # Mostra a lista dinamicamente
                    messagebox.showinfo("Sucesso", f"Foram encontrados {len(data)} exames.")
                else:
                    messagebox.showwarning("Aviso", "Nenhum exame cadastrado.")
            else:
                messagebox.showerror("Erro", "Erro ao buscar dados.")
        except Exception as e:
            messagebox.showerror("Erro", str(e))

    def call_api_get_by_id(self):
        id_exame = self.entry_id.get().strip()
        if not id_exame:
            messagebox.showwarning("Aviso", "Informe um ID no campo correspondente para buscar.")
            return
        try:
            response = requests.get(API_URL)
            if response.status_code == 200:
                data = response.json()
                encontrado = False
                for e in data:
                    if str(e.get("id_exame")) == id_exame:
                        self.preencher_campos(e)
                        encontrado = True
                        messagebox.showinfo("Sucesso", f"Exame ID {id_exame} carregado!")
                        break
                if not encontrado:
                    messagebox.showwarning("Não encontrado", f"Nenhum exame com o ID {id_exame} foi localizado.")
            else:
                messagebox.showerror("Erro", "Erro ao acessar o servidor.")
        except Exception as e:
            messagebox.showerror("Erro", str(e))

    def call_api_post(self):
        valor_str = self.entry_valor.get().strip()

        if not valor_str:
            return messagebox.showwarning("Erro de Validação", "Requisito do Sistema: Informe o valor do exame!")
        
        try:
            valor = float(valor_str)
            if valor <= 0:
                return messagebox.showwarning("Erro de Validação", " O valor do exame deve ser maior que zero!")
        except ValueError:
            return messagebox.showwarning("Erro de Validação", "O valor deve ser um número decimal válido!")
        
        try:
            data = {
                "nome": self.entry_nome.get(),
                "descricao": self.entry_descricao.get(),
                "valor": valor,
                "id_consulta": int(self.entry_consulta.get() or 0)
            }
            response = requests.post(API_URL, json=data)

            if response.status_code in [200, 201]:
                res_json = response.json()
                messagebox.showinfo("Sucesso", res_json.get("mensagem", "Exame cadastrado!"))
                self.clear_fields()
            else:
                erro_detalhe = response.json().get("detail", response.text)
                messagebox.showerror("Erro de Validação", erro_detalhe)
        except Exception as e:
            messagebox.showerror("Erro", "Verifique se os campos numéricos e o ID da consulta estão corretos.")

    def call_api_put(self):
        try:
            id_exame = self.entry_id.get()
            if not id_exame:
                messagebox.showwarning("Aviso", "Informe o ID do exame para editar")
                return

            data = {
                "nome": self.entry_nome.get(),
                "descricao": self.entry_descricao.get(),
                "valor": float(self.entry_valor.get() or 0),
                "id_consulta": int(self.entry_consulta.get() or 0)
            }
            response = requests.put(f"{API_URL}/{id_exame}", json=data)

            if response.status_code in [200, 201]:
                messagebox.showinfo("Sucesso", "Exame atualizado com sucesso")
                self.clear_fields()
            else:
                erro_detalhe = response.json().get("detail", response.text)
                messagebox.showerror("Erro", erro_detalhe)
        except Exception as e:
            messagebox.showerror("Erro", str(e))

    def call_api_delete(self):
        id_exame = self.entry_id.get()
        if not id_exame:
            messagebox.showwarning("Aviso", "Informe o ID do exame")
            return

        try:
            response = requests.delete(f"{API_URL}/{id_exame}")
            if response.status_code == 200:
                messagebox.showinfo("Sucesso", "Exame removido com sucesso")
                self.clear_fields()
            else:
                erro_detalhe = response.json().get("detail", response.text)
                messagebox.showerror("Erro", erro_detalhe)
        except Exception as e:
            messagebox.showerror("Erro", str(e))


if __name__ == "__main__":
    root = tk.Tk()
    app = ClinicaExameApp(root)
    root.mainloop()