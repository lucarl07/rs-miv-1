import { ref, onUnmounted } from 'vue'

export default function useWebSocket(url) {
  const status = ref('disconnected')   // 'connected' | 'disconnected' | 'reconnecting'
  const messages = ref([])
  let ws = null
  let reconnectTimer = null

  function connect() {
    ws = new WebSocket(url)

    ws.onopen = () => {
      status.value = 'connected'
      // console.log("Conectado!")
      clearTimeout(reconnectTimer)
    }

    ws.onmessage = (event) => {
      const payload = JSON.parse(event.data)
      messages.value.push(payload)
    }

    ws.onclose = () => {
      status.value = 'reconnecting'
      // Tenta reconectar após 3 segundos
      reconnectTimer = setTimeout(connect, 3000)
    }

    ws.onerror = () => {
      ws.close() // dispara onclose, que já cuida da reconexão
    }
  }

  function send(content, nickname) {
    if (ws?.readyState === WebSocket.OPEN) {
      ws.send(JSON.stringify({ content, nickname, timestamp: new Date().toISOString() }))
    }
  }

  function disconnect() {
    clearTimeout(reconnectTimer)
    ws?.close()
    status.value = 'disconnected'
  }

  onUnmounted(disconnect)

  connect() // inicia ao montar o componente que usa o composable

  return { status, messages, send, disconnect }
}
