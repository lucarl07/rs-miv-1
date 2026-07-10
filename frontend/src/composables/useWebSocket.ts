import { ref, onUnmounted } from 'vue'

import useAuth from '@/composables/useAuth.ts'

const WS_URL = import.meta.env.VITE_WS_URL
const HEARTBEAT_INTERVAL_MS = 12000
const RECONNECT_INTERVAL_MS = 3000
const INTENTIONAL_DISCONNECT_CODE = 4000

const WS_STATUS_TYPES = ['Desconectado', 'Reconectando', 'Conectado'] as const
type WebSocketStatus = typeof WS_STATUS_TYPES[number]

export default function useWebSocket() {
  const status = ref<WebSocketStatus>(WS_STATUS_TYPES[0])
  const messages = ref<ChatMessageData[]>([])
  const onlineUsers = ref<string[]>([])

  let ws: WebSocket | null = null
  let reconnectTimer: any = null
  let heartbeatTimer: any = null

  function sendRaw(payload: SentMessage) {
    if (ws?.readyState === WebSocket.OPEN) {
      ws.send(JSON.stringify(payload))
    }
  }

  function startHeartbeat() {
    stopHeartbeat() // Evita duplicar o interval em caso de reconexão
    heartbeatTimer = setInterval(() => {
      sendRaw({ type: 'heartbeat' })
    }, HEARTBEAT_INTERVAL_MS)
  }

  function stopHeartbeat() {
    clearInterval(heartbeatTimer)
    heartbeatTimer = null
  }

  function connect() {
    const { token } = useAuth()

    if (!token.value) {
      return;
    }

    ws = new WebSocket(`${WS_URL}/ws?token=${token.value}`)

    ws.onopen = () => {
      status.value = WS_STATUS_TYPES[2]
      console.log('Conectado!')
      clearTimeout(reconnectTimer)
      startHeartbeat()
    }

    ws.onmessage = (event) => {
      const payload: ReceivedMessage = JSON.parse(event.data)

      if (payload.type === 'online_users') {
        onlineUsers.value = payload.users
        return // Retorna por não enviar nada visível no chat em si.
      }

      if (payload.type === 'message_history') {
        for (const i_payload of payload.messages) {
          messages.value.push(i_payload.data)
        }
        return // Retorna, pois já readiciona todas as mensagens recebidas no chat.
      }

      if (payload.type === 'connection' && payload.event === 'join'
        && !onlineUsers.value.includes(payload.nickname)
        // ↑ Evita duplicidade ao receber uma mensagem de join duplicada
      ) {
        onlineUsers.value.push(payload.nickname)
      }

      if (payload.type === 'connection' && payload.event === 'leave') {
        onlineUsers.value = onlineUsers.value.filter(u => u !== payload.nickname)
      }

      messages.value.push(payload.data)
    }

    ws.onclose = (event) => {
      stopHeartbeat()

      if (event.code === INTENTIONAL_DISCONNECT_CODE) {
        console.log(`Desconectado (${event.reason}).`)
        return // Fechamento intencional
      }

      status.value = WS_STATUS_TYPES[2]
      reconnectTimer = setTimeout(connect, RECONNECT_INTERVAL_MS)
      console.log('Desconectado. Tentando reconexão.')
    }

    ws.onerror = () => {
      ws!.close()
    }
  }

  function send(content: string) {
    sendRaw({ content })
  }

  function disconnect() {
    clearTimeout(reconnectTimer)
    ws?.close(INTENTIONAL_DISCONNECT_CODE, 'logout')
    status.value = WS_STATUS_TYPES[0]
  }

  onUnmounted(disconnect)

  connect() // inicia ao montar o componente que usa o composable

  return { status, messages, onlineUsers, send, disconnect }
}
