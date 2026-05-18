<script setup lang="ts">
  import Message from "./Message.vue"
  import MessageInput from "./MessageInput.vue"
  import useWebSocket from "../composables/useWebSocket.js"

  const _messages = [
    // Array demonstrativa apenas; O template usará os dados recebidos pela API.
    {
      id: '10aec4a9-805b-456d-9bf2-2807aec1e783',
      nickname: 'Fulano de Tal',
      content: "Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry's standard dummy text ever since the 1500s, when an unknown printer took a galley of type and scrambled it to make a type specimen book.",
      timestamp: new Date().toISOString()
    },
  ]

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

