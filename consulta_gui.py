# FILE: consulta_gui.py
import tkinter as tk
from tkinter import messagebox
import requests

API_URL = "http://127.0.0.1:8000/consultas"

class ClinicaConsultaApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Sistema Veterinário - Gestão de Consultas")
        self.root.geometry("780x480") 
        self.root.configure(bg="#f5f6fa")
        self.root.resizable(False, False)

        self.setup_ui()

    def setup_ui(self):
        title = tk.Label(self.root, text="Tela de Consultas", font=("Segoe UI", 24, "bold"), bg="#f5f6fa", fg="#2d3436")
        title.pack(pady=(15, 10))

        form_frame = tk.Frame(self.root, bg="#f5f6fa")
        form_frame.pack(padx=40, fill="x")

        # ID CONSULTA
        lbl_id = tk.Label(form_frame, text="ID Consulta:", font=("Segoe UI", 11, "bold"), bg="#f5f6fa", fg="#2d3436")
        lbl_id.grid(row=0, column=0, sticky="w", pady=5)
        id_container = tk.Frame(form_frame, bg="#f5f6fa")
        id_container.grid(row=0, column=1, padx=20, pady=5, sticky="w")
        self.entry_id = tk.Entry(id_container, font=("Segoe UI", 11), relief="solid", bd=1, width=15)
        self.entry_id.pack(side="left", ipady=4)

        # DATA
        lbl_data = tk.Label(form_frame, text="Data (DD/MM/AAAA):", font=("Segoe UI", 11, "bold"), bg="#f5f6fa", fg="#2d3436")
        lbl_data.grid(row=1, column=0, sticky="w", pady=5)
        self.entry_data = tk.Entry(form_frame, font=("Segoe UI", 11), relief="solid", bd=1, width=45)
        self.entry_data.grid(row=1, column=1, padx=20, pady=5, ipady=4)

        # HORA
        lbl_hora = tk.Label(form_frame, text="Hora (HH:MM):", font=("Segoe UI", 11, "bold"), bg="#f5f6fa", fg="#2d3436")
        lbl_hora.grid(row=2, column=0, sticky="w", pady=5)
        self.entry_hora = tk.Entry(form_frame, font=("Segoe UI", 11), relief="solid", bd=1, width=45)
        self.entry_hora.grid(row=2, column=1, padx=20, pady=5, ipady=4)

        # DIAGNÓSTICO
        lbl_diag = tk.Label(form_frame, text="Diagnóstico:", font=("Segoe UI", 11, "bold"), bg="#f5f6fa", fg="#2d3436")
        lbl_diag.grid(row=3, column=0, sticky="w", pady=5)
        self.entry_diagnostico = tk.Entry(form_frame, font=("Segoe UI", 11), relief="solid", bd=1, width=45)
        self.entry_diagnostico.grid(row=3, column=1, padx=20, pady=5, ipady=4)

        # TRATAMENTO
        lbl_trat = tk.Label(form_frame, text="Tratamento:", font=("Segoe UI", 11, "bold"), bg="#f5f6fa", fg="#2d3436")
        lbl_trat.grid(row=4, column=0, sticky="w", pady=5)
        self.entry_tratamento = tk.Entry(form_frame, font=("Segoe UI", 11), relief="solid", bd=1, width=45)
        self.entry_tratamento.grid(row=4, column=1, padx=20, pady=5, ipady=4)

        # ID ANIMAL
        lbl_ani = tk.Label(form_frame, text="ID do Animal:", font=("Segoe UI", 11, "bold"), bg="#f5f6fa", fg="#2d3436")
        lbl_ani.grid(row=5, column=0, sticky="w", pady=5)
        self.entry_animal = tk.Entry(form_frame, font=("Segoe UI", 11), relief="solid", bd=1, width=45)
        self.entry_animal.grid(row=5, column=1, padx=20, pady=5, ipady=4)

        # ID VET
        lbl_v = tk.Label(form_frame, text="ID do Vet:", font=("Segoe UI", 11, "bold"), bg="#f5f6fa", fg="#2d3436")
        lbl_v.grid(row=6, column=0, sticky="w", pady=5)
        self.entry_vet = tk.Entry(form_frame, font=("Segoe UI", 11), relief="solid", bd=1, width=45)
        self.entry_vet.grid(row=6, column=1, padx=20, pady=5, ipady=4)

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
        self.lbl_lista = tk.Label(self.root, text="Consultas Agendadas:", font=("Segoe UI", 11, "bold"), bg="#f5f6fa", fg="#2d3436")
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
        self.root.geometry("780x480")

    def clear_fields(self):
        self.entry_id.delete(0, tk.END)
        self.entry_data.delete(0, tk.END)
        self.entry_hora.delete(0, tk.END)
        self.entry_diagnostico.delete(0, tk.END)
        self.entry_tratamento.delete(0, tk.END)
        self.entry_animal.delete(0, tk.END)
        self.entry_vet.delete(0, tk.END)
        self.esconder_lista_visual()

    def preencher_campos(self, c):
        self.entry_id.delete(0, tk.END)
        self.entry_id.insert(0, c.get("id_consulta", ""))
        self.entry_data.delete(0, tk.END)
        self.entry_data.insert(0, c.get("data", ""))
        self.entry_hora.delete(0, tk.END)
        self.entry_hora.insert(0, c.get("hora", ""))
        self.entry_diagnostico.delete(0, tk.END)
        self.entry_diagnostico.insert(0, c.get("diagnostico", ""))
        self.entry_tratamento.delete(0, tk.END)
        self.entry_tratamento.insert(0, c.get("tratamento", ""))
        self.entry_animal.delete(0, tk.END)
        self.entry_animal.insert(0, c.get("id_animal", ""))
        self.entry_vet.delete(0, tk.END)
        self.entry_vet.insert(0, c.get("id_veterinario", ""))

    def on_select_item(self, event):
        widget = event.widget
        selection = widget.curselection()
        if selection:
            index = selection[0]
            texto = widget.get(index)
            try:
                id_c = texto.split("|")[0].replace("ID:", "").strip()
                response = requests.get(API_URL)
                if response.status_code == 200:
                    for c in response.json():
                        if str(c.get("id_consulta")) == id_c:
                            self.preencher_campos(c)
                            break
            except Exception: pass

    def call_api_get_all(self):
        try:
            response = requests.get(API_URL)
            if response.status_code == 200:
                data = response.json()
                self.listbox.delete(0, tk.END)
                if data:
                    for c in data:
                        txt = f"ID: {c.get('id_consulta'):<4} | Data: {c.get('data'):<10} | Hora: {c.get('hora'):<6} | Diag: {c.get('diagnostico'):<12} | Vet ID: {c.get('id_veterinario')}"
                        self.listbox.insert(tk.END, txt)
                    self.mostrar_lista_visual()
                    messagebox.showinfo("Sucesso", f"Foram encontradas {len(data)} consultas.")
                else: messagebox.showwarning("Aviso", "Nenhuma consulta agendada.")
        except Exception as e: messagebox.showerror("Erro", str(e))

    def call_api_get_by_id(self):
        id_c = self.entry_id.get().strip()
        if not id_c: return messagebox.showwarning("Aviso", "Informe um ID.")
        try:
            response = requests.get(API_URL)
            if response.status_code == 200:
                for c in response.json():
                    if str(c.get("id_consulta")) == id_c:
                        self.preencher_campos(c)
                        return messagebox.showinfo("Sucesso", "Consulta carregada!")
                messagebox.showwarning("Erro", "Não encontrada.")
        except Exception as e: messagebox.showerror("Erro", str(e))

    def call_api_post(self):
        data_str = self.entry_data.get().strip()
        hora_str = self.entry_hora.get().strip()
        diagnostico = self.entry_diagnostico.get().strip()
        tratamento = self.entry_tratamento.get().strip()
        id_animal_str = self.entry_animal.get().strip()
        id_vet_str = self.entry_vet.get().strip()

      
        if not data_str or not hora_str:
            return messagebox.showwarning("Erro de Validação", "Requisito 9: A data e a hora da consulta devem ser preenchidas!")
        
       
        if not diagnostico or not tratamento:
            return messagebox.showwarning("Erro de Validação", "Requisito 10: Os campos Diagnóstico e Tratamento devem ser preenchidos!")

        if not id_animal_str or not id_vet_str:
            return messagebox.showwarning("Erro de Validação", "Informe os IDs do Animal e do Veterinário!")

        try:
            id_animal = int(id_animal_str)
            id_vet = int(id_vet_str)
        except ValueError:
            return messagebox.showwarning("Erro de Validação", "Os IDs devem ser números inteiros!")

     
        try:
            checar_agenda = requests.get(API_URL)
            if checar_agenda.status_code == 200:
                for consulta in checar_agenda.json():
                    if (consulta.get("id_veterinario") == id_vet) and (consulta.get("data") == data_str) and (consulta.get("hora") == hora_str):
                        return messagebox.showerror(
                            "Conflito de Agenda", 
                            f"Requisito 9: O Veterinário ID {id_vet} já possui uma consulta no dia {data_str} às {hora_str}!"
                        )
        except Exception:
            pass

        
        try:
            data = {
                "data_str": data_str,
                "hora_str": hora_str,
                "diagnostico": diagnostico,
                "tratamento": tratamento,
                "id_animal": id_animal,
                "id_veterinario": id_vet
            }
            res = requests.post(API_URL, json=data)
            if res.status_code in [200, 201]:
                messagebox.showinfo("Sucesso", "Consulta agendada com sucesso!")
                self.clear_fields()
            else: messagebox.showerror("Erro", res.text)
        except Exception as e: messagebox.showerror("Erro", str(e))

    def call_api_put(self):
        id_c = self.entry_id.get()
        if not id_c: return messagebox.showwarning("Aviso", "Informe o ID.")
        try:
            data = {
                "data_str": self.entry_data.get(),
                "hora_str": self.entry_hora.get(),
                "diagnostico": self.entry_diagnostico.get(),
                "tratamento": self.entry_tratamento.get(),
                "id_animal": int(self.entry_animal.get() or 0),
                "id_veterinario": int(self.entry_vet.get() or 0)
            }
            res = requests.put(f"{API_URL}/{id_c}", json=data)
            if res.status_code in [200, 201]:
                messagebox.showinfo("Sucesso", "Consulta atualizada!")
                self.clear_fields()
            else: messagebox.showerror("Erro", res.text)
        except Exception as e: messagebox.showerror("Erro", str(e))

    def call_api_delete(self):
        id_c = self.entry_id.get()
        if not id_c: return messagebox.showwarning("Aviso", "Informe o ID.")
        try:
            res = requests.delete(f"{API_URL}/{id_c}")
            if res.status_code == 200:
                messagebox.showinfo("Sucesso", "Consulta removida!")
                self.clear_fields()
            else: messagebox.showerror("Erro", res.text)
        except Exception as e: messagebox.showerror("Erro", str(e))

if __name__ == "__main__":
    root = tk.Tk()
    app = ClinicaConsultaApp(root)
    root.mainloop()# FILE: consulta_gui.py
import tkinter as tk
from tkinter import messagebox
import requests

API_URL = "http://127.0.0.1:8000/consultas"

class ClinicaConsultaApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Sistema Veterinário - Gestão de Consultas")
        self.root.geometry("780x480") # Ajustado para os novos campos
        self.root.configure(bg="#f5f6fa")
        self.root.resizable(False, False)

        self.setup_ui()

    def setup_ui(self):
        title = tk.Label(self.root, text="Tela de Consultas", font=("Segoe UI", 24, "bold"), bg="#f5f6fa", fg="#2d3436")
        title.pack(pady=(15, 10))

        form_frame = tk.Frame(self.root, bg="#f5f6fa")
        form_frame.pack(padx=40, fill="x")

        # ID CONSULTA
        lbl_id = tk.Label(form_frame, text="ID Consulta:", font=("Segoe UI", 11, "bold"), bg="#f5f6fa", fg="#2d3436")
        lbl_id.grid(row=0, column=0, sticky="w", pady=5)
        id_container = tk.Frame(form_frame, bg="#f5f6fa")
        id_container.grid(row=0, column=1, padx=20, pady=5, sticky="w")
        self.entry_id = tk.Entry(id_container, font=("Segoe UI", 11), relief="solid", bd=1, width=15)
        self.entry_id.pack(side="left", ipady=4)

        # DATA
        lbl_data = tk.Label(form_frame, text="Data (DD/MM/AAAA):", font=("Segoe UI", 11, "bold"), bg="#f5f6fa", fg="#2d3436")
        lbl_data.grid(row=1, column=0, sticky="w", pady=5)
        self.entry_data = tk.Entry(form_frame, font=("Segoe UI", 11), relief="solid", bd=1, width=45)
        self.entry_data.grid(row=1, column=1, padx=20, pady=5, ipady=4)

        # HORA
        lbl_hora = tk.Label(form_frame, text="Hora (HH:MM):", font=("Segoe UI", 11, "bold"), bg="#f5f6fa", fg="#2d3436")
        lbl_hora.grid(row=2, column=0, sticky="w", pady=5)
        self.entry_hora = tk.Entry(form_frame, font=("Segoe UI", 11), relief="solid", bd=1, width=45)
        self.entry_hora.grid(row=2, column=1, padx=20, pady=5, ipady=4)

        # DIAGNÓSTICO
        lbl_diag = tk.Label(form_frame, text="Diagnóstico:", font=("Segoe UI", 11, "bold"), bg="#f5f6fa", fg="#2d3436")
        lbl_diag.grid(row=3, column=0, sticky="w", pady=5)
        self.entry_diagnostico = tk.Entry(form_frame, font=("Segoe UI", 11), relief="solid", bd=1, width=45)
        self.entry_diagnostico.grid(row=3, column=1, padx=20, pady=5, ipady=4)

        # TRATAMENTO
        lbl_trat = tk.Label(form_frame, text="Tratamento:", font=("Segoe UI", 11, "bold"), bg="#f5f6fa", fg="#2d3436")
        lbl_trat.grid(row=4, column=0, sticky="w", pady=5)
        self.entry_tratamento = tk.Entry(form_frame, font=("Segoe UI", 11), relief="solid", bd=1, width=45)
        self.entry_tratamento.grid(row=4, column=1, padx=20, pady=5, ipady=4)

        # ID ANIMAL
        lbl_ani = tk.Label(form_frame, text="ID do Animal:", font=("Segoe UI", 11, "bold"), bg="#f5f6fa", fg="#2d3436")
        lbl_ani.grid(row=5, column=0, sticky="w", pady=5)
        self.entry_animal = tk.Entry(form_frame, font=("Segoe UI", 11), relief="solid", bd=1, width=45)
        self.entry_animal.grid(row=5, column=1, padx=20, pady=5, ipady=4)

        # ID VET
        lbl_v = tk.Label(form_frame, text="ID do Vet:", font=("Segoe UI", 11, "bold"), bg="#f5f6fa", fg="#2d3436")
        lbl_v.grid(row=6, column=0, sticky="w", pady=5)
        self.entry_vet = tk.Entry(form_frame, font=("Segoe UI", 11), relief="solid", bd=1, width=45)
        self.entry_vet.grid(row=6, column=1, padx=20, pady=5, ipady=4)

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
        self.lbl_lista = tk.Label(self.root, text="Consultas Agendadas:", font=("Segoe UI", 11, "bold"), bg="#f5f6fa", fg="#2d3436")
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
        self.root.geometry("780x480")

    def clear_fields(self):
        self.entry_id.delete(0, tk.END)
        self.entry_data.delete(0, tk.END)
        self.entry_hora.delete(0, tk.END)
        self.entry_diagnostico.delete(0, tk.END)
        self.entry_tratamento.delete(0, tk.END)
        self.entry_animal.delete(0, tk.END)
        self.entry_vet.delete(0, tk.END)
        self.esconder_lista_visual()

    def preencher_campos(self, c):
        self.entry_id.delete(0, tk.END)
        self.entry_id.insert(0, c.get("id_consulta", ""))
        self.entry_data.delete(0, tk.END)
        self.entry_data.insert(0, c.get("data", ""))
        self.entry_hora.delete(0, tk.END)
        self.entry_hora.insert(0, c.get("hora", ""))
        self.entry_diagnostico.delete(0, tk.END)
        self.entry_diagnostico.insert(0, c.get("diagnostico", ""))
        self.entry_tratamento.delete(0, tk.END)
        self.entry_tratamento.insert(0, c.get("tratamento", ""))
        self.entry_animal.delete(0, tk.END)
        self.entry_animal.insert(0, c.get("id_animal", ""))
        self.entry_vet.delete(0, tk.END)
        self.entry_vet.insert(0, c.get("id_veterinario", ""))

    def on_select_item(self, event):
        widget = event.widget
        selection = widget.curselection()
        if selection:
            index = selection[0]
            texto = widget.get(index)
            try:
                id_c = texto.split("|")[0].replace("ID:", "").strip()
                response = requests.get(API_URL)
                if response.status_code == 200:
                    for c in response.json():
                        if str(c.get("id_consulta")) == id_c:
                            self.preencher_campos(c)
                            break
            except Exception: pass

    def call_api_get_all(self):
        try:
            response = requests.get(API_URL)
            if response.status_code == 200:
                data = response.json()
                self.listbox.delete(0, tk.END)
                if data:
                    for c in data:
                        txt = f"ID: {c.get('id_consulta'):<4} | Data: {c.get('data'):<10} | Hora: {c.get('hora'):<6} | Diag: {c.get('diagnostico'):<12} | Vet ID: {c.get('id_veterinario')}"
                        self.listbox.insert(tk.END, txt)
                    self.mostrar_lista_visual()
                    messagebox.showinfo("Sucesso", f"Foram encontradas {len(data)} consultas.")
                else: messagebox.showwarning("Aviso", "Nenhuma consulta agendada.")
        except Exception as e: messagebox.showerror("Erro", str(e))

    def call_api_get_by_id(self):
        id_c = self.entry_id.get().strip()
        if not id_c: return messagebox.showwarning("Aviso", "Informe um ID.")
        try:
            response = requests.get(API_URL)
            if response.status_code == 200:
                for c in response.json():
                    if str(c.get("id_consulta")) == id_c:
                        self.preencher_campos(c)
                        return messagebox.showinfo("Sucesso", "Consulta carregada!")
                messagebox.showwarning("Erro", "Não encontrada.")
        except Exception as e: messagebox.showerror("Erro", str(e))

    def call_api_post(self):
        data_str = self.entry_data.get().strip()
        hora_str = self.entry_hora.get().strip()
        diagnostico = self.entry_diagnostico.get().strip()
        tratamento = self.entry_tratamento.get().strip()
        id_animal_str = self.entry_animal.get().strip()
        id_vet_str = self.entry_vet.get().strip()

        # 🛡️ Requisito 9: Validação de preenchimento
        if not data_str or not hora_str:
            return messagebox.showwarning("Erro de Validação", "Requisito 9: A data e a hora da consulta devem ser preenchidas!")
        
        # 🛡️ Requisito 10: Prontuário Obrigatório (Diagnóstico/Tratamento)
        if not diagnostico or not tratamento:
            return messagebox.showwarning("Erro de Validação", "Requisito 10: Os campos Diagnóstico e Tratamento devem ser preenchidos!")

        if not id_animal_str or not id_vet_str:
            return messagebox.showwarning("Erro de Validação", "Informe os IDs do Animal e do Veterinário!")

        try:
            id_animal = int(id_animal_str)
            id_vet = int(id_vet_str)
        except ValueError:
            return messagebox.showwarning("Erro de Validação", "Os IDs devem ser números inteiros!")

        # 🛡️ TRAVA DO REQUISITO 9: Evitar Choque de Horário (Comparando data E hora separadas)
        try:
            checar_agenda = requests.get(API_URL)
            if checar_agenda.status_code == 200:
                for consulta in checar_agenda.json():
                    if (consulta.get("id_veterinario") == id_vet) and (consulta.get("data") == data_str) and (consulta.get("hora") == hora_str):
                        return messagebox.showerror(
                            "Conflito de Agenda", 
                            f"Requisito 9: O Veterinário ID {id_vet} já possui uma consulta no dia {data_str} às {hora_str}!"
                        )
        except Exception:
            pass

        # Enviando os parâmetros exatos esperados pelo seu controller
        try:
            data = {
                "data_str": data_str,
                "hora_str": hora_str,
                "diagnostico": diagnostico,
                "tratamento": tratamento,
                "id_animal": id_animal,
                "id_veterinario": id_vet
            }
            res = requests.post(API_URL, json=data)
            if res.status_code in [200, 201]:
                messagebox.showinfo("Sucesso", "Consulta agendada com sucesso!")
                self.clear_fields()
            else: messagebox.showerror("Erro", res.text)
        except Exception as e: messagebox.showerror("Erro", str(e))

    def call_api_put(self):
        id_c = self.entry_id.get()
        if not id_c: return messagebox.showwarning("Aviso", "Informe o ID.")
        try:
            data = {
                "data_str": self.entry_data.get(),
                "hora_str": self.entry_hora.get(),
                "diagnostico": self.entry_diagnostico.get(),
                "tratamento": self.entry_tratamento.get(),
                "id_animal": int(self.entry_animal.get() or 0),
                "id_veterinario": int(self.entry_vet.get() or 0)
            }
            res = requests.put(f"{API_URL}/{id_c}", json=data)
            if res.status_code in [200, 201]:
                messagebox.showinfo("Sucesso", "Consulta atualizada!")
                self.clear_fields()
            else: messagebox.showerror("Erro", res.text)
        except Exception as e: messagebox.showerror("Erro", str(e))

    def call_api_delete(self):
        id_c = self.entry_id.get()
        if not id_c: return messagebox.showwarning("Aviso", "Informe o ID.")
        try:
            res = requests.delete(f"{API_URL}/{id_c}")
            if res.status_code == 200:
                messagebox.showinfo("Sucesso", "Consulta removida!")
                self.clear_fields()
            else: messagebox.showerror("Erro", res.text)
        except Exception as e: messagebox.showerror("Erro", str(e))

if __name__ == "__main__":
    root = tk.Tk()
    app = ClinicaConsultaApp(root)
    root.mainloop()