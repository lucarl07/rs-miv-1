// Dependências Externas
import { ref, computed } from "vue";
import { useRouter } from "vue-router";

// Chamadas à API
import registerUser from "@/api/registerUser";
import loginAsUser from "@/api/loginAsUser";

// Outros Composables
import usePgpIdentity from "@/composables/usePgpIdentity";

const TOKEN_KEY = 'access_token'
const token = ref<string | null>(sessionStorage.getItem(TOKEN_KEY))

export default function useAuth() {
  const router = useRouter()
  const { ensureKeyPair, removeKeyPair } = usePgpIdentity()

  const isAuthenticated = computed(() => token.value !== null)

  async function login(email: string, password: string): Promise<void> {
    const payload = { email, password }
    const data = await loginAsUser(payload)
    // TODO (p/o back-end): Decodificar o JWT no cliente, porque tá precário viu

    await ensureKeyPair(data.access_token)
    // ↑ PGP deve ser validado antes do token ser persistido.

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
    router.push('/login')
    token.value = null
    sessionStorage.removeItem(TOKEN_KEY)
    removeKeyPair()
  }

  return { token, isAuthenticated, login, register, logout }
}
