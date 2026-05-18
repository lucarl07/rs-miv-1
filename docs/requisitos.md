# RS-MIV-1: Levantamento de Requisitos

Um projeto de Luiz Carlos Jr. ([lucarl07](https://github.com/lucarl07))

---

## Requisitos Funcionais

### GESTÃO DE CONEXÃO E IDENTIFICAÇÃO:
- [ ] **Cadastro e Autenticação:** Todos os usuários na plataforma devem estar registrados em uma conta com nome/apelido, email e senha.
- [X] **Canal Global:** Os usuários serão conectados automaticamente ao canal global assim que o apelido for definido.
- [X] **Notificação de Presença:** O sistema deve exibir uma mensagem automática para todos os usuários informando quando um novo participante entrou ou saiu do chat.

### MENSAGERIA EM TEMPO REAL:
- [X] **Envio de mensagens:** Usuários devem poder redigir e enviar mensagens de texto.
- [X] **Recebimento de mensagens:** A interface de todos os usuários conectados deve ser atualizada com a nova mensagem recebida, sem atualizar a página.
- [X] **Identificação de autoria:** Cada mensagem exibida deve estar acompanhada do apelido do remetente e do horário do envio (timestamp).

### INTERFACE E FEEDBACK:
- [B] **Histórico Local Volátil:** O sistema deve manter o histórico das mensagens enviadas e recebidas durante a sessão atual (enquanto a aba estiver aberta).
- [B] **Limpeza de Input:** O sistema deve limpar o campo de digitação imediatamente após o envio bem-sucedido de uma mensagem.

### CONTROLE DE ESTADO:
- [ ] **Visualização de Status:** O sistema deve exibir um indicador visual mostrando se o usuário está atualmente conectado ao servidor de WebSockets.

### OPCIONAIS:
- [ ] **Notificações Push:** O sistema deve exibir notificações push no navegador, caso desejado pelo usuário.
- [ ] **Permissões Hierárquicas:** Dentro dos grupos haverão 3 cargos: o membro comum; o moderador, que possui poderes moderativos como remover membros comuns do grupo; e o líder, que tem todos os poderes do moderador, além de poder adicioná-los e removê-los, e é irremovível.

## Requisitos Não Funcionais

- [ ] **Entrega de mensagens em tempo real:** Idealmente <=200ms em uma rede local estável.
- [ ] **Persistência de Conexão:** Através da WebSocket API nativa do navegador.
- [ ] **Feedback de Estado:** O usuário deve saber se está "Conectado" ou "Desconectado"
- [ ] **Sanitização de Dados:** Impedir o envio de códigos maliciosos (ex.: `<script>`) que execute em outro navegador (proteção contra XSS).
- [ ] **Criptografia E2E:** O sistema deve implementar criptografia end-to-end através de pares de chaves PGP.
- [ ] **Autenticação segura:** Autenticação realizada através de JSON Web Tokens e OAuth 2.0.
- [ ] **Modularidade:** Separar claramente a lógica do servidor da lógica do cliente.
- [ ] **Responsividade:** Deve funcionar minimamente bem tanto no desktop quanto no celular.
- [ ] **Indicadores Visuais:** Diferenciação clara entre mensagens enviadas e recebidas.
