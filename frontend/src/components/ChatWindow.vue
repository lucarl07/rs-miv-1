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
  <main class="my-10 w-4/5 md:w-9/10 mx-auto">
    <ol class="flex flex-col gap-10">
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
          :username="message.nickname"
          :content="message.content"
          :timestamp="message.timestamp"
          />
      </li>
    </ol>
    <MessageInput @send="handleSend"/>
  </main>
</template>

