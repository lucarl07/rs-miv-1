<script setup lang="ts">
  import Message from "./Message.vue"
  import MessageInput from "./MessageInput.vue"
  import useWebSocket from "../composables/useWebSocket.js"

  const nickname = "luiz"
  const { status, messages, send } = useWebSocket(`ws://localhost:8000/ws?nickname=${nickname}`)

  const handleSend = (payload) => send(payload, nickname)
</script>

<template>
  <main>
    <ol>
      <li v-for="(message, index) in messages" :key="message.id">
        <!--
          Lógica primitiva para diferenciar mensagens do sistema
          de mensagens de usuários (no momento, sem distinção):
        -->
        <Message v-if="message.nickname !== '%sys%'"
          :username="message.nickname"
          :content="message.content"
          :timestamp="message.timestamp"
          />
        <Message v-else
          :username="message.nickname"
          :content="message.content"
          :timestamp="message.timestamp"
          />
      </li>
    </ol>
    <MessageInput @send="handleSend"/>
  </main>
</template>

