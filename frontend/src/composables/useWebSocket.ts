import { ref, onUnmounted } from 'vue'

import useAuth from '@/composables/useAuth.ts'
import { usePgpIdentity } from './usePgpIdentity'
import { useSessionKey } from './useSessionKey'
import { decryptMessage, encryptMessage } from '@/utils/messageCrypto'

const WS_URL = import.meta.env.VITE_WS_URL
const HEARTBEAT_INTERVAL_MS = 12000
const RECONNECT_INTERVAL_MS = 3000
const INTENTIONAL_DISCONNECT_CODE = 4000

const WS_STATUS_TYPES = ['Desconectado', 'Reconectando', 'Conectado'] as const
type WebSocketStatus = typeof WS_STATUS_TYPES[number]

export default function useWebSocket() {
  const { decryptSessionKey } = usePgpIdentity()
  const { setSessionKey, getSessionKey } = useSessionKey()

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

  async function addToMessageHistory(
    msgData: ChatMessageData,
    isContentEncrypted: boolean = true
  ) {
    if (!isContentEncrypted) {
      messages.value.push(msgData)
      return;
    }

    const key = getSessionKey()
    if (!key) {
      console.error('Mensagem recebida, mas K ainda não disponível — descartada.')
      return
    }

    const decryptedContent = await decryptMessage(msgData.content, key)
    messages.value.push({ ...msgData, content: decryptedContent })
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

    ws.onmessage = async (event) => {
      const payload: ReceivedMessage = JSON.parse(event.data)

      /* --- MENSAGENS OPERACIONAIS --- */

      if (payload.type === 'key_envelope') {
        try {
          const key = await decryptSessionKey(payload.encrypted_key)
          setSessionKey(key)
        } catch (err) {
          console.error('Falha ao decifrar a chave de sessão K:', err)
        }
        return
      }
      if (payload.type === 'online_users') {
        onlineUsers.value = payload.users
        return
      }

      /* --- HISTÓRICO DE MENSAGENS (MSGS. DE USUÁRIO AGRUPADAS) --- */

      if (payload.type === 'message_history') {
        for (const i_payload of payload.messages) {
          await addToMessageHistory(i_payload.data)
        }
        return
      }

      /* --- MENSAGENS DO CHAT (SISTEMA & USUÁRIO) --- */

      let isContentEncrypted = true // Padrão para mensagens do usuário

      if (payload.type === 'connection') {
        if (
          payload.event === 'join' &&
          !onlineUsers.value.includes(payload.nickname)
          // ↑ Evita exibir mensagens de join duplicadas
        ) {
          onlineUsers.value.push(payload.nickname)
        }
        if (payload.event === 'leave') {
          onlineUsers.value = onlineUsers.value.filter(u => u !== payload.nickname)
        }
        isContentEncrypted = false
      }

      await addToMessageHistory(payload.data, isContentEncrypted)
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

  async function send(content: string) {
    const key = getSessionKey()
    if (!key) {
      console.error('Chave de sessão K ainda não disponível — mensagem não enviada.')
      return
    }

    const encryptedContent = await encryptMessage(content, key)
    sendRaw({ content: encryptedContent })
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
