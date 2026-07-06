/* TODO: Trocar a extensão do arquivo para .ts e fazer tipagem TypeScript */

import { ref, onUnmounted } from 'vue'

import useAuth from '@/composables/useAuth.ts'

const WS_URL = import.meta.env.VITE_WS_URL
const HEARTBEAT_INTERVAL_MS = 12000
const RECONNECT_INTERVAL_MS = 3000
const INTENTIONAL_DISCONNECT_CODE = 4000

export default function useWebSocket() {
  const status = ref('disconnected')   // 'connected' | 'disconnected' | 'reconnecting'
  const messages = ref([])
  const onlineUsers = ref([])

  let ws = null
  let reconnectTimer = null
  let heartbeatTimer = null

  function sendRaw(payload) {
    if (ws?.readyState === WebSocket.OPEN) {
      ws.send(JSON.stringify(payload))
    }
  }

  function startHeartbeat() {
    stopHeartbeat() // evita duplicar o interval em caso de reconexão
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
      status.value = 'connected'
      console.log('Conectado!')
      clearTimeout(reconnectTimer)
      startHeartbeat()
    }

    ws.onmessage = (event) => {
      const payload = JSON.parse(event.data)

      if (payload.type === 'online_users') {
        onlineUsers.value = payload.users
        return
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

      status.value = 'reconnecting'
      reconnectTimer = setTimeout(connect, RECONNECT_INTERVAL_MS)
      console.log('Desconectado. Tentando reconexão.')
    }

    ws.onerror = () => {
      ws.close()
    }
  }

  function send(content) {
    sendRaw({ content })
  }

  function disconnect() {
    clearTimeout(reconnectTimer)
    ws?.close(INTENTIONAL_DISCONNECT_CODE, 'logout')
    status.value = 'disconnected'
  }

  onUnmounted(disconnect)

  connect() // inicia ao montar o componente que usa o composable

  return { status, messages, onlineUsers, send, disconnect }
}
