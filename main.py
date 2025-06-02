from models.Carro import Carro
from models.Moto import Moto
from models.Caminhao import Caminhao
from models.Proprietario import Proprietario
from utils.erros import *
import tkinter as tk
from tkinter import ttk, messagebox
import re
from datetime import datetime

# Classe principal
class SistemaVeiculos:
    def __init__(self, root):
        self.root = root
        self.root.title("Sistema de Cadastro de Veículos")
        self.root.geometry("1000x800")
        self.root.resizable(True, True)

        self.veiculos = []
        self.proprietarios = [] 

        self.container = tk.Frame(root)
        self.container.pack(fill="both", expand=True)

        self.container.grid_rowconfigure(0, weight=1)
        self.container.grid_columnconfigure(0, weight=1)

        self.tela_principal = tk.Frame(self.container)
        self.tela_cadastro = tk.Frame(self.container)
        self.tela_listagem = tk.Frame(self.container)
        self.tela_cadastro_proprietario = tk.Frame(self.container)
        self.tela_listagem_proprietarios = tk.Frame(self.container) 

        for tela in (self.tela_principal, self.tela_cadastro, self.tela_listagem,
                     self.tela_cadastro_proprietario, self.tela_listagem_proprietarios): 
            tela.grid(row=0, column=0, sticky="nsew")

        self.configurar_tela_principal()
        self.configurar_tela_cadastro()
        self.configurar_tela_listagem()
        self.configurar_tela_cadastro_proprietario() 
        self.configurar_tela_listagem_proprietarios()

        self.mostrar_tela(self.tela_principal)
    
    def mostrar_tela(self, tela):
        tela.tkraise()
    
    def configurar_tela_principal(self):
        frame = tk.Frame(self.tela_principal, padx=20, pady=20)
        frame.place(relx=0.5, rely=0.5, anchor="center")

        titulo = tk.Label(frame, text="SISTEMA DE CADASTRO DE VEÍCULOS", font=("Arial", 16, "bold"))
        titulo.pack(pady=(0, 30))

        btn_cadastrar_veiculo = tk.Button(frame, text="Cadastrar Novo Veículo", width=25, height=2,
                                         command=lambda: self.mostrar_tela(self.tela_cadastro))
        btn_cadastrar_veiculo.pack(pady=10)

        btn_listar_veiculos = tk.Button(frame, text="Listar Veículos", width=25, height=2,
                                        command=lambda: self.atualizar_listagem())
        btn_listar_veiculos.pack(pady=10)

        
        btn_cadastrar_proprietario = tk.Button(frame, text="Cadastrar Novo Proprietário", width=25, height=2,
                                               command=lambda: self.mostrar_tela(self.tela_cadastro_proprietario))
        btn_cadastrar_proprietario.pack(pady=10)

        btn_listar_proprietarios = tk.Button(frame, text="Listar Proprietários", width=25, height=2,
                                             command=lambda: self.atualizar_listagem_proprietarios())
        btn_listar_proprietarios.pack(pady=10)

        btn_sair = tk.Button(frame, text="Sair", width=25, height=2,
                             command=self.root.quit)
        btn_sair.pack(pady=10)
    
    def configurar_tela_cadastro_proprietario(self):
        titulo = tk.Label(self.tela_cadastro_proprietario, text="CADASTRO DE PROPRIETÁRIO", font=("Arial", 16, "bold"))
        titulo.pack(pady=20)

        form_frame = tk.Frame(self.tela_cadastro_proprietario, padx=20)
        form_frame.pack(fill="both")

        tk.Label(form_frame, text="Nome:").grid(row=0, column=0, sticky="e", pady=5)
        self.proprietario_nome_entry = tk.Entry(form_frame, width=30)
        self.proprietario_nome_entry.grid(row=0, column=1, sticky="w", pady=5)

        tk.Label(form_frame, text="CPF:").grid(row=1, column=0, sticky="e", pady=5)
        self.proprietario_cpf_entry = tk.Entry(form_frame, width=15)
        self.proprietario_cpf_entry.grid(row=1, column=1, sticky="w", pady=5)

       
        tk.Label(form_frame, text="Adicionar Veículo (opcional):").grid(row=2, column=0, sticky="e", pady=5)
        self.veiculo_proprietario_combo = ttk.Combobox(form_frame, values=[], state="readonly", width=30)
        self.veiculo_proprietario_combo.grid(row=2, column=1, sticky="w", pady=5)

        
        add_veiculo_btn = tk.Button(form_frame, text="Adicionar Veículo à Lista",
                                    command=self.adicionar_veiculo_ao_proprietario_temp)
        add_veiculo_btn.grid(row=3, column=1, sticky="w", pady=5)

        
        tk.Label(form_frame, text="Veículos Adicionados:").grid(row=4, column=0, sticky="ne", pady=5)
        self.proprietario_veiculos_listbox = tk.Listbox(form_frame, height=5, width=40)
        self.proprietario_veiculos_listbox.grid(row=4, column=1, sticky="w", pady=5)
        
        
        self.temp_proprietario_placas = []

        botoes_frame = tk.Frame(self.tela_cadastro_proprietario)
        botoes_frame.pack(pady=20)

        tk.Button(botoes_frame, text="Cancelar", width=10,
                  command=lambda: self.mostrar_tela(self.tela_principal)).pack(side="left", padx=10)

        tk.Button(botoes_frame, text="Salvar", width=10,
                  command=self.salvar_proprietario).pack(side="left", padx=10)

    def adicionar_veiculo_ao_proprietario_temp(self):
        selected_placa = self.veiculo_proprietario_combo.get()
        if selected_placa and selected_placa not in self.temp_proprietario_placas:
            self.temp_proprietario_placas.append(selected_placa)
            self.proprietario_veiculos_listbox.insert(tk.END, selected_placa)
        elif selected_placa in self.temp_proprietario_placas:
            messagebox.showwarning("Veículo já adicionado", "Esta placa já foi adicionada a este proprietário.")
        else:
            messagebox.showinfo("Aviso", "Selecione um veículo para adicionar.")

    def atualizar_combo_veiculos_proprietario(self):
        
        self.veiculo_proprietario_combo['values'] = []
        if self.veiculos:
            
            plates = [v.get_placa() for v in self.veiculos]
            self.veiculo_proprietario_combo['values'] = plates
            if plates:
                self.veiculo_proprietario_combo.set(plates[0]) 
    def salvar_proprietario(self):
        nome = self.proprietario_nome_entry.get().strip()
        cpf = self.proprietario_cpf_entry.get().strip()

        if not nome or not cpf:
            messagebox.showwarning("Dados incompletos", "Preencha todos os campos obrigatórios!")
            return

        
        if any(p.cpf == re.sub(r'\D', '', cpf) for p in self.proprietarios):
            messagebox.showwarning("CPF duplicado", "Já existe um proprietário cadastrado com este CPF.")
            return

        try:
            proprietario = Proprietario(nome, cpf)
            
            for placa in self.temp_proprietario_placas:
                proprietario.adicionar_veiculo(placa)

            self.proprietarios.append(proprietario)
            messagebox.showinfo("Sucesso", "Proprietário cadastrado com sucesso!")

            
            self.proprietario_nome_entry.delete(0, "end")
            self.proprietario_cpf_entry.delete(0, "end")
            self.proprietario_veiculos_listbox.delete(0, "end")
            self.temp_proprietario_placas = []

            self.mostrar_tela(self.tela_principal)

        except CPFInvalidoError as e:
            messagebox.showwarning("CPF Inválido", str(e))
        except ValueError as e:
            messagebox.showwarning("Erro de Validação", str(e))
        except Exception as e:
            messagebox.showerror("Erro", f"Ocorreu um erro ao salvar o proprietário: {e}")
    
    def configurar_tela_listagem_proprietarios(self):
        titulo = tk.Label(self.tela_listagem_proprietarios, text="PROPRIETÁRIOS CADASTRADOS", font=("Arial", 16, "bold"))
        titulo.pack(pady=20)

        lista_frame = tk.Frame(self.tela_listagem_proprietarios, padx=20)
        lista_frame.pack(fill="both", expand=True, pady=10)

        scrollbar = tk.Scrollbar(lista_frame)
        scrollbar.pack(side="right", fill="y")

        self.listbox_proprietarios = tk.Listbox(lista_frame, width=90, height=10, font=("Arial", 10))
        self.listbox_proprietarios.pack(side="left", fill="both", expand=True)

        self.listbox_proprietarios.config(yscrollcommand=scrollbar.set)
        scrollbar.config(command=self.listbox_proprietarios.yview)

        botoes_frame = tk.Frame(self.tela_listagem_proprietarios)
        botoes_frame.pack(pady=15)

        tk.Button(botoes_frame, text="Ver Detalhes", width=12,
                  command=self.ver_detalhes_proprietario).pack(side="left", padx=5)

        tk.Button(botoes_frame, text="Voltar", width=12,
                  command=lambda: self.mostrar_tela(self.tela_principal)).pack(side="left", padx=5)

    def atualizar_listagem_proprietarios(self):
        self.listbox_proprietarios.delete(0, "end")
        for proprietario in self.proprietarios:
            self.listbox_proprietarios.insert("end", str(proprietario))
        self.mostrar_tela(self.tela_listagem_proprietarios)

    def ver_detalhes_proprietario(self):
        selecionado = self.listbox_proprietarios.curselection()
        if not selecionado:
            messagebox.showinfo("Aviso", "Selecione um proprietário para ver os detalhes")
            return

        proprietario = self.proprietarios[selecionado[0]]
        detalhes = str(proprietario)
        messagebox.showinfo("Detalhes do Proprietário", detalhes)
    
    def configurar_tela_cadastro(self):
        # Título
        titulo = tk.Label(self.tela_cadastro, text="CADASTRO DE VEÍCULO", font=("Arial", 16, "bold"))
        titulo.pack(pady=20)
        
        # Frame para o formulário
        form_frame = tk.Frame(self.tela_cadastro, padx=20)
        form_frame.pack(fill="both")
        
        # Campos comuns
        tk.Label(form_frame, text="Placa:").grid(row=0, column=0, sticky="e", pady=5)
        self.placa_entry = tk.Entry(form_frame, width=15)
        self.placa_entry.grid(row=0, column=1, sticky="w", pady=5)
        
        tk.Label(form_frame, text="Marca:").grid(row=1, column=0, sticky="e", pady=5)
        self.marca_entry = tk.Entry(form_frame, width=20)
        self.marca_entry.grid(row=1, column=1, sticky="w", pady=5)
        
        tk.Label(form_frame, text="Modelo:").grid(row=2, column=0, sticky="e", pady=5)
        self.modelo_entry = tk.Entry(form_frame, width=20)
        self.modelo_entry.grid(row=2, column=1, sticky="w", pady=5)
        
        tk.Label(form_frame, text="Ano:").grid(row=3, column=0, sticky="e", pady=5)
        self.ano_entry = tk.Entry(form_frame, width=6)
        self.ano_entry.grid(row=3, column=1, sticky="w", pady=5)
        
        # Seletor de tipo de veículo
        tk.Label(form_frame, text="Tipo:").grid(row=4, column=0, sticky="e", pady=5)
        self.tipo_var = tk.StringVar(value="Carro")
        
        tipo_frame = tk.Frame(form_frame)
        tipo_frame.grid(row=4, column=1, sticky="w", pady=5)
        
        tk.Radiobutton(tipo_frame, text="Carro", variable=self.tipo_var, value="Carro",
                     command=self.mostrar_campos_especificos).pack(side="left")
        tk.Radiobutton(tipo_frame, text="Moto", variable=self.tipo_var, value="Moto",
                     command=self.mostrar_campos_especificos).pack(side="left")
        tk.Radiobutton(tipo_frame, text="Caminhão", variable=self.tipo_var, value="Caminhao",
                     command=self.mostrar_campos_especificos).pack(side="left")
        
        # Frame para campos específicos
        self.campos_especificos_frame = tk.Frame(form_frame)
        self.campos_especificos_frame.grid(row=5, column=0, columnspan=2, pady=10)
        
        # Campos específicos para Carro
        self.frame_carro = tk.Frame(self.campos_especificos_frame)
        tk.Label(self.frame_carro, text="Número de Portas:").pack(side="left")
        self.portas_entry = tk.Entry(self.frame_carro, width=5)
        self.portas_entry.pack(side="left", padx=5)
        
        # Campos específicos para Moto
        self.frame_moto = tk.Frame(self.campos_especificos_frame)
        tk.Label(self.frame_moto, text="Cilindrada (cc):").pack(side="left")
        self.cilindrada_entry = tk.Entry(self.frame_moto, width=7)
        self.cilindrada_entry.pack(side="left", padx=5)
        
        # Campos específicos para Caminhão
        self.frame_caminhao = tk.Frame(self.campos_especificos_frame)
        tk.Label(self.frame_caminhao, text="Capacidade de Carga (kg):").pack(side="left")
        self.capacidade_entry = tk.Entry(self.frame_caminhao, width=10)
        self.capacidade_entry.pack(side="left", padx=5)
        
        # Mostrar os campos iniciais (Carro)
        self.mostrar_campos_especificos()
        
        # Botões de ação
        botoes_frame = tk.Frame(self.tela_cadastro)
        botoes_frame.pack(pady=20)
        
        tk.Button(botoes_frame, text="Cancelar", width=10,
                command=lambda: self.mostrar_tela(self.tela_principal)).pack(side="left", padx=10)
        
        tk.Button(botoes_frame, text="Salvar", width=10,
                command=self.salvar_veiculo).pack(side="left", padx=10)
    
    def mostrar_campos_especificos(self):
        # Esconder todos os frames de campos específicos
        self.frame_carro.pack_forget()
        self.frame_moto.pack_forget()
        self.frame_caminhao.pack_forget()
        
        # Mostrar apenas o frame correspondente ao tipo selecionado
        tipo = self.tipo_var.get()
        if tipo == "Carro":
            self.frame_carro.pack()
        elif tipo == "Moto":
            self.frame_moto.pack()
        elif tipo == "Caminhao":
            self.frame_caminhao.pack()
    
    def configurar_tela_listagem(self):
        # Título
        titulo = tk.Label(self.tela_listagem, text="VEÍCULOS CADASTRADOS", font=("Arial", 16, "bold"))
        titulo.pack(pady=20)
        
        # Frame para filtro
        filtro_frame = tk.Frame(self.tela_listagem)
        filtro_frame.pack(fill="x", padx=20, pady=5)
        
        tk.Label(filtro_frame, text="Filtrar por tipo:").pack(side="left")
        self.filtro_var = tk.StringVar(value="Todos")
        filtro_combo = ttk.Combobox(filtro_frame, textvariable=self.filtro_var, 
                                  values=["Todos", "Carro", "Moto", "Caminhão"], width=15)
        filtro_combo.pack(side="left", padx=5)
        
        filtro_btn = tk.Button(filtro_frame, text="Filtrar", command=self.filtrar_veiculos)
        filtro_btn.pack(side="left", padx=5)
        
        # Frame para a lista
        lista_frame = tk.Frame(self.tela_listagem, padx=20)
        lista_frame.pack(fill="both", expand=True, pady=10)
        
        # Scrollbar
        scrollbar = tk.Scrollbar(lista_frame)
        scrollbar.pack(side="right", fill="y")
        
        # Listbox
        self.listbox = tk.Listbox(lista_frame, width=70, height=10, font=("Arial", 10))
        self.listbox.pack(side="left", fill="both", expand=True)
        
        # Configura scrollbar
        self.listbox.config(yscrollcommand=scrollbar.set)
        scrollbar.config(command=self.listbox.yview)
        
        # Botões
        botoes_frame = tk.Frame(self.tela_listagem)
        botoes_frame.pack(pady=15)
        
        tk.Button(botoes_frame, text="Ver Detalhes", width=12,
                command=self.ver_detalhes).pack(side="left", padx=5)
        
        tk.Button(botoes_frame, text="Voltar", width=12,
                command=lambda: self.mostrar_tela(self.tela_principal)).pack(side="left", padx=5)
    
    def salvar_veiculo(self):
        # Obter dados comuns
        placa = self.placa_entry.get().strip().upper()
        marca = self.marca_entry.get().strip()
        modelo = self.modelo_entry.get().strip()
        ano_str = self.ano_entry.get().strip()
        tipo = self.tipo_var.get()
        
        # Validar campos obrigatórios
        if not placa or not marca or not modelo or not ano_str:
            messagebox.showwarning("Dados incompletos", "Preencha todos os campos obrigatórios!")
            return
        
        # Validar formato da placa (ABC1234 ou ABC1D23)
        if not re.match(r'^[A-Z]{3}[0-9][0-9A-Z][0-9]{2}$', placa):
            messagebox.showwarning("Placa inválida", "A placa deve seguir o padrão ABC1234 ou ABC1D23")
            return
        
        # Validar ano
        try:
            ano = int(ano_str)
            ano_atual = datetime.now().year
            if ano < 1900 or ano > ano_atual + 1:
                messagebox.showwarning("Ano inválido", f"O ano deve estar entre 1900 e {ano_atual + 1}")
                return
        except ValueError:
            messagebox.showwarning("Ano inválido", "O ano deve ser um número")
            return
        
        # Criar o veículo do tipo específico
        if tipo == "Carro":
            num_portas_str = self.portas_entry.get().strip()
            if not num_portas_str:
                messagebox.showwarning("Dados incompletos", "Informe o número de portas")
                return
            try:
                num_portas = int(num_portas_str)
                if num_portas < 1 or num_portas > 5:
                    messagebox.showwarning("Valor inválido", "O número de portas deve estar entre 1 e 5")
                    return
                veiculo = Carro(placa, marca, modelo, ano, num_portas)
            except ValueError:
                messagebox.showwarning("Valor inválido", "O número de portas deve ser um número")
                return
                
        elif tipo == "Moto":
            cilindrada_str = self.cilindrada_entry.get().strip()
            if not cilindrada_str:
                messagebox.showwarning("Dados incompletos", "Informe a cilindrada")
                return
            try:
                cilindrada = int(cilindrada_str)
                if cilindrada < 50 or cilindrada > 2000:
                    messagebox.showwarning("Valor inválido", "A cilindrada deve estar entre 50 e 2000 cc")
                    return
                veiculo = Moto(placa, marca, modelo, ano, cilindrada)
            except ValueError:
                messagebox.showwarning("Valor inválido", "A cilindrada deve ser um número")
                return
                
        elif tipo == "Caminhao":
            capacidade_str = self.capacidade_entry.get().strip()
            if not capacidade_str:
                messagebox.showwarning("Dados incompletos", "Informe a capacidade de carga")
                return
            try:
                capacidade = float(capacidade_str)
                if capacidade <= 0:
                    messagebox.showwarning("Valor inválido", "A capacidade de carga deve ser maior que zero")
                    return
                veiculo = Caminhao(placa, marca, modelo, ano, capacidade)
            except ValueError:
                messagebox.showwarning("Valor inválido", "A capacidade de carga deve ser um número")
                return
        
        # Adicionar o veículo à lista
        self.veiculos.append(veiculo)
        messagebox.showinfo("Sucesso", "Veículo cadastrado com sucesso!")
        self.atualizar_combo_veiculos_proprietario()
        
        # Limpar campos
        self.placa_entry.delete(0, "end")
        self.marca_entry.delete(0, "end")
        self.modelo_entry.delete(0, "end")
        self.ano_entry.delete(0, "end")
        self.portas_entry.delete(0, "end")
        self.cilindrada_entry.delete(0, "end")
        self.capacidade_entry.delete(0, "end")
        
        # Voltar para a tela principal
        self.mostrar_tela(self.tela_principal)
    
    def atualizar_listagem(self):
        # Atualizar a listagem e mostrar a tela
        self.filtrar_veiculos()
        self.mostrar_tela(self.tela_listagem)
    
    def filtrar_veiculos(self):
        # Limpar a lista
        self.listbox.delete(0, "end")
        
        # Filtrar veículos pelo tipo
        filtro = self.filtro_var.get()
        
        for veiculo in self.veiculos:
            if filtro == "Todos":
                self.listbox.insert("end", str(veiculo))
            elif filtro == "Carro" and isinstance(veiculo, Carro):
                self.listbox.insert("end", str(veiculo))
            elif filtro == "Moto" and isinstance(veiculo, Moto):
                self.listbox.insert("end", str(veiculo))
            elif filtro == "Caminhão" and isinstance(veiculo, Caminhao):
                self.listbox.insert("end", str(veiculo))
    
    def ver_detalhes(self):
        # Obter o índice selecionado
        selecionado = self.listbox.curselection()
        if not selecionado:
            messagebox.showinfo("Aviso", "Selecione um veículo para ver os detalhes")
            return
        
        # Obter o veículo correspondente à seleção
        filtro = self.filtro_var.get()
        veiculos_filtrados = []
        
        for veiculo in self.veiculos:
            if filtro == "Todos":
                veiculos_filtrados.append(veiculo)
            elif filtro == "Carro" and isinstance(veiculo, Carro):
                veiculos_filtrados.append(veiculo)
            elif filtro == "Moto" and isinstance(veiculo, Moto):
                veiculos_filtrados.append(veiculo)
            elif filtro == "Caminhão" and isinstance(veiculo, Caminhao):
                veiculos_filtrados.append(veiculo)
        
        veiculo = veiculos_filtrados[selecionado[0]]
        
        # Montar a mensagem de detalhes usando polimorfismo
        detalhes = str(veiculo)
        
        # Adicionar informações específicas
        if isinstance(veiculo, Carro):
            detalhes += f"\nNúmero de Portas: {veiculo.get_num_portas()}"
        elif isinstance(veiculo, Moto):
            detalhes += f"\nCilindrada: {veiculo.get_cilindrada()} cc"
        elif isinstance(veiculo, Caminhao):
            detalhes += f"\nCapacidade de Carga: {veiculo.get_capacidade_carga()} kg"
        
        # Mostrar detalhes
        messagebox.showinfo("Detalhes do Veículo", detalhes)

# Iniciar a aplicação
if __name__ == "__main__":
    root = tk.Tk()
    app = SistemaVeiculos(root)
    root.mainloop()