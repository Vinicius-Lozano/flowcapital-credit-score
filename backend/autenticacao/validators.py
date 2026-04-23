import re
from django.core.exceptions import ValidationError


def validar_cpf(cpf):
    cpf = ''.join(filter(str.isdigit, cpf))
    if len(cpf) != 11 or len(set(cpf)) == 1:
        return False
    for i, peso_inicial in enumerate([10, 11]):
        soma = sum(int(cpf[j]) * (peso_inicial - j) for j in range(i + 9))
        resto = (soma * 10) % 11
        if resto in (10, 11):
            resto = 0
        if resto != int(cpf[9 + i]):
            return False
    return True


class SenhaRobustaValidator:
    def validate(self, password, user=None):
        erros = []
        if not re.search(r'[A-Z]', password):
            erros.append('pelo menos uma letra maiúscula')
        if not re.search(r'[a-z]', password):
            erros.append('pelo menos uma letra minúscula')
        if not re.search(r'\d', password):
            erros.append('pelo menos um número')
        if not re.search(r'[!@#$%^&*()\-_=+\[\]{};:\'",.<>?/\\|`~]', password):
            erros.append('pelo menos um símbolo especial')
        if erros:
            raise ValidationError(f'A senha deve conter {", ".join(erros)}.')

    def get_help_text(self):
        return 'A senha deve conter letras maiúsculas, minúsculas, números e símbolos especiais.'
