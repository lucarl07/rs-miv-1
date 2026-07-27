/// <reference types="vite/client" />

//#region |=== Tipos padrão do Vue ===|

interface ImportMetaEnv {
  readonly VITE_API_URL: string
  readonly VITE_WS_URL: string
}

interface ImportMeta {
  readonly env: ImportMetaEnv
}

//#endregion

//#region |==== Criptografia ====|

type _PGPUnknownKeyPairName = 'unknown'

type PGPKeyPairName = UserId | _PGPUnknownKeyPairName

type PGPSessionKey = Uint8Array | null

//#endregion

//#region |=== Identificadores (UUIDs) ===|

type UserId = string & { readonly _userId: unique symbol }

type MessageId = string & { readonly _messageId: unique symbol }

//#endregion

//#region |=== Validação de Formulário ===|

type AsyncFieldEvalStatus =
  'idle'        // Aguardando avaliação
  | 'checking'  // Sendo avaliado
  | 'available' // Resposta: disponível
  | 'taken'     // Resposta: indisponível
  | 'invalid'   // Não enviado, pois é inválido

interface SignupFormErrors {
  nickname: string | null
  email: string | null
  password: string | null
  confirmPassword: string | null
  other?: string | null
}

//#region |=== API (Payloads e Respostas HTTP) ===|

interface RegisterUserPayload {
  nickname: string
  email: string
  password: string
}

type RegisterUserResponse = Promise<void>

interface LoginPayload {
  email: string
  password: string
}

interface LoginResponse {
  access_token: string
  token_type: string
}

interface CurrentUserResponse {
  id: string
  nickname: string
  email: string
  created_at: any
}

interface CurrentUserInfo extends CurrentUserResponse {}

//#endregion

//#region |=== Chat (Broadcasts WebSocket) ===|

// |--- Mensagens Recebidas ---|

interface ChatMessageData {
  id: MessageId
  nickname: string
  content: string
  timestamp: string
}
interface UserMessage {
  type: 'message'
  data: ChatMessageData
}
interface SystemMessage {
  type: 'connection'
  event: 'join' | 'leave'
  nickname: string
  data: ChatMessageData
}
type ChatMessage = UserMessage | SystemMessage

interface KeyEnvelope {
  type: 'key_envelope'
  encrypted_key: string
}

interface MessageHistory {
  type: 'message_history'
  messages: ChatMessage[]
}

interface OnlineUsers {
  type: 'online_users'
  users: string[]
}

type ReceivedMessage =
  ChatMessage
  | KeyEnvelope
  | MessageHistory
  | OnlineUsers

// |--- Mensagens Enviadas ---|

interface HeartbeatMessage {
  type: 'heartbeat'
}

interface SentUserMessage {
  content: string
}

type SentMessage = HeartbeatMessage | SentUserMessage

//#endregion

