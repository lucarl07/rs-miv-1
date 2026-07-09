import nh3

msg_sanitizer = nh3.Cleaner(tags=set()) 
"""Sanitizador de todos os tipos de mensagem."""
# ---
# Por enquanto, nenhuma tag HTML será permitida. Possivelmente isso mude no
# futuro, caso eu decida liberar formatação HTML nas mensagens, permitir 
# envio de snippets de código, etc.
# ---

