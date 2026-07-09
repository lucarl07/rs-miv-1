import nh3

msg_cleaner = nh3.Cleaner(tags=set())
# Por enquanto, nenhuma tag HTML será permitida.
#
# Possivelmente isso mude no futuro, caso eu decida liberar formatação
# HTML nas mensagens, permitir envio de snippets de código, etc.

