import re
import string

def check_nickname_validity(nickname: str) -> None:
    NICKNAME_PATTERN = re.compile(r"^[a-zA-Z0-9_-]{5,30}$")

    if not NICKNAME_PATTERN.match(nickname):
        raise ValueError("""
            Nickname deve conter apenas letras, números, '_' ou '-', entre
            5 e 30 caracteres.
        """)

def check_pw_validity(password: str) -> None:
    SPECIAL_CHARS = string.punctuation # Caracteres: !"#$%&'()*+,-./:;<=>?@[\]^_`{|}~
    ESCAPED_SPECIALS = re.escape(SPECIAL_CHARS)

    PASSWORD_PATTERN = re.compile(
        r"^"                           # Começo da string
        r"(?=.*[a-z])"                 # Ao menos uma letra minúscula
        r"(?=.*[A-Z])"                 # Ao menos uma letra maiúscula
        r"(?=.*\d)"                    # Ao menos um número
        f"(?=.*[{ESCAPED_SPECIALS}])"  # Ao menos um dos caracteres especiais válidos
        f"[A-Za-z\\d{ESCAPED_SPECIALS}]" # Lista total de todos os caracteres válidos
        r"{8,}"                        # Tamanho mínimo de 8 caracteres
        r"$"                           # Fim da string
    )   
    # ↑ CERTIFIQUE-SE: A última string concatenada deve começar com 'r', 
    # para que o todo seja interpretado como uma regex e não string comum.

    if not PASSWORD_PATTERN.match(password):
        raise ValueError("""
            Senha deve conter 8 caracteres, entre eles letras maiúsculas e 
            minúsculas, dígitos e caracteres especiais.
        """)

