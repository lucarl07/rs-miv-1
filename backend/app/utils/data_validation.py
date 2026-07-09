import re

def check_nickname_validity(nickname: str) -> None:
    NICKNAME_PATTERN = re.compile(r"^[a-zA-Z0-9_-]{5,30}$")

    if not NICKNAME_PATTERN.match(nickname):
        raise ValueError(
            "Nickname deve conter apenas letras, números, '_' ou '-', entre 5 e 30 caracteres."
        )

def check_pw_validity(password: str) -> None:
    """Verifica os requisitos da senha e lança um erro específico se falhar."""
    
    if len(password) < 8:
        raise ValueError("A senha deve ter pelo menos 8 caracteres")
    
    if not re.search(r"[A-Z]", password):
        raise ValueError("A senha deve conter pelo menos uma letra maiúscula")
        
    if not re.search(r"[a-z]", password):
        raise ValueError("A senha deve conter pelo menos uma letra minúscula")
        
    if not re.search(r"\d", password):
        raise ValueError("A senha deve conter pelo menos um número")
        
    if not re.search(r"[\[\]\s_!@#$%^&*(),.?\":{}|<>]", password):
        raise ValueError("A senha deve conter pelo menos um caractere especial")
