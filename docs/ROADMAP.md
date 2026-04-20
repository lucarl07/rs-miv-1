# ROADMAP DE DESENVOLVIMENTO — RS-MIV-1

Um guia de implementação em fases para o projeto de chat em tempo real.

**Stack:** Vue 3 + Tailwind CSS · FastAPI + asyncio · PostgreSQL/SQLite · Redis · WebSocket (RFC 6455)

---

## Estratégia Geral: De Dentro para Fora

Construir o **core funcional primeiro** (sem UI elaborada), validar que tudo funciona, e só depois polir a interface. Isso evita o erro clássico de ter um front bonito com um back instável.

---

## Fase 1 — Back-end: Esqueleto WebSocket

> **Sprint 1** · Prioridade: Alta · Pré-requisito de tudo

O coração do sistema. Nada mais deve ser implementado antes disso estar estável.

**O que implementar:**

- Projeto FastAPI com endpoint `/ws` aceitando conexões WebSocket
- Classe `ConnectionManager` com métodos `connect`, `disconnect` e `broadcast`
- Broadcast de mensagens com payload JSON (`nickname`, `content`, `timestamp`)
- Notificações de presença automáticas (`"X entrou no chat"` / `"X saiu"`)
  - Fecha os RFs: **Notificação de Presença** e **Controle de Estado**
- SQLite (dev) com SQLAlchemy — apenas a tabela `messages` por ora

> ⚠️ **Não implemente autenticação ainda.** Use `nickname` como query param (`/ws?nickname=luiz`) para validar o fluxo antes de adicionar JWT.

---

## Fase 2 — Front-end: Vue 3 Funcional

> **Sprint 1 / início do Sprint 2** · Prioridade: Alta · Depende da Fase 1

Com o back rodando, conectar o Vue 3 ao servidor.

**O que implementar:**

- Composable `useWebSocket` — encapsula o `WebSocket` nativo, gerencia reconexão e expõe estado reativo (`status: 'connected' | 'disconnected'`)
- Componente de chat básico: lista de mensagens + campo de input + botão de envio
- Indicador visual de status de conexão
  - Fecha o RF: **Visualização de Status**
- Limpeza do input pós-envio e histórico volátil de sessão
  - Fecha os RFs: **Limpeza de Input** e **Histórico Local Volátil**

> Tailwind entra aqui para montar o layout, mas sem perfeccionismo visual ainda.

---

## Fase 3 — Autenticação

> **Sprint 2** · Prioridade: Alta · Depende da Fase 2

Só após o chat estar funcionando de ponta a ponta.

**O que implementar:**

- Tabela `users` no banco (`nickname`, `email`, senha com `bcrypt`)
- Endpoints de registro e login retornando JWT
- Token enviado no header do handshake WebSocket (ou como query param no upgrade request)
- No front: tela de login/cadastro, armazenamento do JWT
  - Fecha o RF: **Cadastro e Autenticação**
  - Fecha o RNF: **Autenticação Segura (JWT)**

> OAuth 2.0 pode ser adicionado em iteração posterior — começar apenas com JWT próprio.

---

## Fase 4 — Redis + Presença

> **Sprint 2 / Sprint 3** · Prioridade: Média · Depende da Fase 3

**O que implementar:**

- Redis para rastrear usuários online (chave `presence:{user_id}` com TTL)
- Cache das últimas N mensagens para novos usuários que entram no canal
  - Fecha o RF: **Canal Global**

---

## Fase 5 — Segurança e Requisitos Não Funcionais

> **Sprint 3** · Prioridade: Média-Alta · Depende das Fases anteriores

**Proteção contra XSS:**

- Sanitizar conteúdo das mensagens no back-end antes de persistir/broadcast
- No front, usar `v-text` em vez de `v-html` — nunca interpolar HTML diretamente
  - Fecha o RNF: **Sanitização de Dados**

**Criptografia E2E (PGP):**

- Geração de par de chaves no cliente
- Troca de chaves públicas via servidor
- Criptografia/descriptografia no browser com [`openpgp.js`](https://openpgpjs.org/)
  - Fecha o RNF: **Criptografia E2E**

> ⚠️ Este é o requisito mais complexo — deixar por último.

---

## O que NÃO implementar prematuramente

| Item | Motivo |
|---|---|
| Permissões Hierárquicas | Opcional que adiciona complexidade de dados e lógica de moderação — distrai do núcleo |
| Redis | Fácil de plugar depois; não configurar antes de ter o WebSocket estável |
| PostgreSQL em produção | SQLite resolve bem durante o desenvolvimento inteiro |
| OAuth 2.0 | Adicionar só após JWT próprio estar funcionando |

---

## Visão Geral das Fases

```
Sprint 1       Sprint 2              Sprint 3
─────────────────────────────────────────────────────
[Fase 1]  →  [Fase 3]  →  [Fase 5 - XSS]
[Fase 2]  →  [Fase 4]  →  [Fase 5 - E2E PGP]
```

---

*Documento gerado com base no levantamento de requisitos `rs-miv-lr.md`.*
