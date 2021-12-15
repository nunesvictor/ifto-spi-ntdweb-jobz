def mask_cep(value):
    if len(value) != 8:
        return value

    return f'{value[:5]}-{value[5:]}'


def mask_cnpj(value):
    if len(value) != 14:
        return value

    return f'{value[:2]}.{value[2:5]}.{value[5:8]}/{value[8:12]}-{value[12:]}'


def mask_cpf(value):
    if len(value) != 11:
        return value

    return f'{value[:3]}.{value[3:6]}.{value[6:9]}-{value[9:]}'

def mask_phone(value):
    if len(value) != 11:
        return value

    return f'({value[:2]}) {value[2:7]}-{value[7:]}'
