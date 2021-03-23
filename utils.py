import re 

def format_percent(porcentagem):
    """
    Função que verifica se o valor passado
    é do tipo 'float',s atisfazendo a condição
    uma máscara é aplicada para normalizar o
    valor percentual.

    Args:
        - porcentagem : Type [float][str]
    """
    if isinstance(porcentagem, float):
        return '{:.2f}%'.format(porcentagem)
    return porcentagem

def format_money(valor):
    """
    Função que utiliza a sintaxe regex para
    identificar se o valor informado corresponde
    ao padrão monetário.
    Não satisfazendo a verificação uma 
    máscara é aplicada para normalizar o
    valor monetário após devidos ajustes.

    Args:
        - valor : Type [str]
    """
    fix_value = valor.replace(" ", "")
    pattern = '[\$]+?(\d+([,\.\d]+)\.\d+)'
    result = re.match(pattern, fix_value)
    if not result:
        vl = int(fix_value.strip('$').replace(',', ''))
        vl_final = '${:0,.2f}'.format(vl)
        return vl_final
    return fix_value
