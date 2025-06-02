# models/Proprietario.py
import re
from utils.erros import CPFInvalidoError, PlacaInvalidaError

class Proprietario:
    def __init__(self, nome, cpf):
        self._nome = None
        self._cpf = None
        self._veiculos_adquiridos = [] # Lista de placas de veículos
        self.nome = nome
        self.cpf = cpf

    @property
    def nome(self):
        return self._nome

    @nome.setter
    def nome(self, value):
        if not isinstance(value, str) or not value.strip():
            raise ValueError("O nome não pode ser vazio.")
        self._nome = value.strip()

    @property
    def cpf(self):
        return self._cpf

    @cpf.setter
    def cpf(self, value):
        self._cpf = self.validar_cpf(value)

    @property
    def veiculos_adquiridos(self):
        return self._veiculos_adquiridos

    def validar_cpf(self, cpf):
        # Remove caracteres não numéricos
        cpf = re.sub(r'\D', '', cpf)

        if len(cpf) != 11:
            raise CPFInvalidoError("CPF deve conter 11 dígitos.")

        # Verifica se todos os dígitos são iguais (ex: 111.111.111-11)
        if cpf == cpf[0] * 11:
            raise CPFInvalidoError("CPF inválido: todos os dígitos são iguais.")

        # Validação do primeiro dígito verificador
        soma = 0
        for i in range(9):
            soma += int(cpf[i]) * (10 - i)
        digito1 = 11 - (soma % 11)
        if digito1 > 9:
            digito1 = 0
        if not (int(cpf[9]) == digito1):
            raise CPFInvalidoError("CPF inválido: primeiro dígito verificador incorreto.")

        # Validação do segundo dígito verificador
        soma = 0
        for i in range(10):
            soma += int(cpf[i]) * (11 - i)
        digito2 = 11 - (soma % 11)
        if digito2 > 9:
            digito2 = 0
        if not (int(cpf[10]) == digito2):
            raise CPFInvalidoError("CPF inválido: segundo dígito verificador incorreto.")

        return cpf

    def adicionar_veiculo(self, placa):
        # Valida o formato da placa (ABC1234 ou ABC1D23)
        if not re.match(r'^[A-Z]{3}[0-9][0-9A-Z][0-9]{2}$', placa.upper()):
            raise PlacaInvalidaError("A placa deve seguir o padrão ABC1234 ou ABC1D23.")
        self._veiculos_adquiridos.append(placa.upper())

    def __str__(self):
        return f"Nome: {self.nome} - CPF: {self.cpf_formatado()} - Veículos: {', '.join(self.veiculos_adquiridos) if self.veiculos_adquiridos else 'Nenhum'}"

    def cpf_formatado(self):
        return f"{self.cpf[:3]}.{self.cpf[3:6]}.{self.cpf[6:9]}-{self.cpf[9:]}"