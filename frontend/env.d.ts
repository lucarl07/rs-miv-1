/// <reference types="vite/client" />

interface ImportMetaEnv {
  readonly VITE_API_URL: string
}

interface ImportMeta {
  readonly env: ImportMetaEnv
}

interface RegisterUserPayload {
  nickname: string
  email: string
  password: string
}

type RegisterUserResponse = Promise<void>
