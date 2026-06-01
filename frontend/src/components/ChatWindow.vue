<script setup lang="ts">
  import Message from "./Message.vue"
  import MessageInput from "./MessageInput.vue"
  import useWebSocket from "../composables/useWebSocket.js"
  import genUniqueNickname from '../utils/genUniqueNickname.ts'

  const nickname = genUniqueNickname("luiz")
  const { status, messages, send } = useWebSocket(`ws://localhost:8000/ws?nickname=${nickname}`)

  const handleSend = (content) => send(content, nickname)
</script>

<template>
  <main class="flex flex-col flex-1 overflow-hidden mx-auto px-1 w-5/8">
    <ol class="flex flex-col flex-1 overflow-y-auto mt-10 h-full">
      <li v-for="(message, index) in messages" :key="message.id" >
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
          username="Mensagem do sistema"
          :content="message.content"
          :timestamp="message.timestamp"
          isSystemMessage="true"
          />
      </li>
    </ol>
    <MessageInput
      @send="handleSend"
      class="mb-10"
    />
  </main>
</template>

