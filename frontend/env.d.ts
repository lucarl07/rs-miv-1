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

interface LoginPayload {
  email: string
  password: string
}

interface LoginResponse {
  access_token: string
  token_type: string
}

interface SignupFormErrors {
  email: string | null
  password: string | null
  confirmPassword: string | null
  other: string | null
}

interface CurrentUserResponse {
  id: string
  nickname: string
  email: string
  created_at: any
}

