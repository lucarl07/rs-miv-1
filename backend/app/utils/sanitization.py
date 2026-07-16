# --- ⚠ FUNCIONALIDADE DEPRECIADA ⚠ ---
# Devido à abordagem de encriptação E2E, as mensagens chegam como texto 
# incompreensível do lado do servidor. Assim, todo o processo de 
# sanitização foi repassado para o cliente.
# 
# Por ora, o arquivo está ainda existe apenas para fins de documentação.

import nh3

msg_sanitizer = nh3.Cleaner(tags=set()) 
"""Sanitizador de todos os tipos de mensagem."""
# ---
# Por enquanto, nenhuma tag HTML será permitida. Possivelmente isso mude no
# futuro, caso eu decida liberar formatação HTML nas mensagens, permitir 
# envio de snippets de código, etc.
# ---

