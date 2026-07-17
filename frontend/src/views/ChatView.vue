<script setup lang="ts">
  // Importações externas e assets:
  import { computed } from 'vue'
  import icon_Exit from "@/assets/icons/exit.png"

  // Componentes:
  import Message from '@/components/Message.vue'
  import MessageInput from '@/components/MessageInput.vue'
  import ChatSidebar from '@/components/ChatSidebar.vue'

  // Composables e outras funções
  import useUserData from '@/composables/useUserData.ts'
  import useAuth from '@/composables/useAuth.ts'
  import useWebSocket from '@/composables/useWebSocket'
  import useAutoScroll from '@/composables/useAutoScroll.ts'
  import useSessionKey from '@/composables/useSessionKey'
  import genUniqueNickname from '@/utils/genUniqueNickname.ts'

  const { sessionKey } = useSessionKey()
  const { logout } = useAuth()
  const { nickname } = useUserData({ loadOnStartup: true })

  const { status, messages, onlineUsers, send, disconnect } = useWebSocket()
  const { scrollTarget } = useAutoScroll(messages.value, () => true)

  const isChatReady = computed<boolean>(() =>
    status.value === 'Conectado' && sessionKey.value !== null
  )

  async function handleSend(content) {
    await send(content)
  }
  function handleLogout() {
    const isConfirmed = confirm("Tem certeza de que você deseja sair?")
    if (!isConfirmed) return;

    disconnect()
    logout()
  }
</script>

<template>
  <div class="flex flex-row flex-1 overflow-hidden">
    <main class="flex flex-col flex-3">
      <ol ref="scrollTarget" class="flex flex-col overflow-y-auto mx-10 mt-10 h-full">
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
        :enableSend="isChatReady"
        class="mb-10 mx-10"
      />
    </main>
    <ChatSidebar
      :nickname="nickname"
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

