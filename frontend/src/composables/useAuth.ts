// Dependências Externas
import { ref, computed } from "vue";

// Chamadas à API
import registerUser from "@/api/registerUser";
import loginAsUser from "@/api/loginAsUser";

const TOKEN_KEY = 'access_token'
const token = ref<string | null>(sessionStorage.getItem(TOKEN_KEY))

export default function useAuth() {
  const isAuthenticated = computed(() => token.value !== null)

  async function login(email: string, password: string): Promise<void> {
    const payload = { email, password }
    const data = await loginAsUser(payload)

    token.value = data.access_token
    sessionStorage.setItem(TOKEN_KEY, data.access_token)
  }

  async function register(
    nickname: string, email: string, password: string
  ): Promise<void> {
    const payload = { nickname, email, password }
    await registerUser(payload)
  }

  function logout(): void {
    token.value = null
    sessionStorage.removeItem(TOKEN_KEY)
  }

  return { token, isAuthenticated, login, register, logout }
}
