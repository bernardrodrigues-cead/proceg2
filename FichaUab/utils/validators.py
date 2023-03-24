from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

def is_cpf_valid(cpf: str) -> bool:
    cpf = ''.join(c for c in cpf if c.isdigit())
    if len(cpf) != 11:
        raise ValidationError(_('CPF inválido'))

    # Get the first 9 digits of the CPF and generate the first 2 verifying digits
    new_cpf = cpf[:9]
    while len(new_cpf) < 11:
        r = sum([int(new_cpf[p]) * (len(new_cpf)+1 - p) for p in range(len(new_cpf))]) % 11
        new_cpf += '0' if r <= 1 else str(11-r)

    # If the generated CPF is equal to the original one, then it's valid
    if new_cpf != cpf:
        raise ValidationError(_('CPF inválido'))
    