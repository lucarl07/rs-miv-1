<script setup lang="ts">
  import Message from '@/components/Message.vue'
  import MessageInput from '@/components/MessageInput.vue'

  import useAuth from '@/composables/useAuth.ts'
  import useWebSocket from '@/composables/useWebSocket.js'
  import genUniqueNickname from '@/utils/genUniqueNickname.ts'

  const { status, messages, send } = useWebSocket()

  const handleSend = (content) => send(content)
</script>

<template>
  <main class="flex flex-col flex-1 overflow-hidden mx-auto px-1 w-5/8">
    <ol class="flex flex-col flex-1 overflow-y-auto mt-10 h-full">
      <li v-for="(message, index) in messages" :key="message.id" >
        <Message v-if="message.nickname !== '%sys%'"
          :username="message.nickname"
          :content="message.content"
          :timestamp="message.timestamp"
          />
        <Message v-else
          username="Mensagem do sistema"
          :content="message.content"
          :timestamp="message.timestamp"
          :isSystemMessage="true"
          />
      </li>
    </ol>
    <MessageInput
      @send="handleSend"
      class="mb-10"
    />
  </main>
</template>

