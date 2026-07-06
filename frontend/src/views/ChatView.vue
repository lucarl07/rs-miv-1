<script setup lang="ts">
  import icon_Exit from "@/assets/icons/exit.png"

  import Message from '@/components/Message.vue'
  import MessageInput from '@/components/MessageInput.vue'
  import ChatSidebar from '@/components/ChatSidebar.vue'

  import useAuth from '@/composables/useAuth.ts'
  import useWebSocket from '@/composables/useWebSocket.js'
  import genUniqueNickname from '@/utils/genUniqueNickname.ts'

  const { status, messages, onlineUsers, send, disconnect } = useWebSocket()
  const { logout } = useAuth()

  const handleSend = (content) => send(content)
  const handleLogout = () => {
    const isConfirmed = confirm("Tem certeza de que você deseja sair?")
    if (!isConfirmed) return;

    disconnect()
    logout()
  }
</script>

<template>
  <div class="flex flex-row flex-1 overflow-hidden">
    <main class="flex flex-col flex-3">
      <ol class="flex flex-col overflow-y-auto mx-10 mt-10 h-full">
        <li v-for="(message, index) in messages" :key="message.id" >
          <Message
            :username="message.nickname"
            :content="message.content"
            :timestamp="message.timestamp"
            />
        </li>
      </ol>
      <MessageInput
        @send="handleSend"
        class="mb-10 mx-10"
      />
    </main>
    <ChatSidebar
      nickname="nomedocarinhaai"
      :status="status"
      :userList="onlineUsers"
      class="flex-1 border-s-2 border-s-crushed-berry"
    >
      <template #options>
        <button @click="handleLogout">
          <img
            :src="icon_Exit"
            alt="Sair do aplicativo"
            class="invert"
          />
        </button>
      </template>
    </ChatSidebar>
  </div>
</template>

