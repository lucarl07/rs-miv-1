// Dependências Externas
import { ref, computed } from "vue";

// Módulos do cliente:
import useAuth from "./useAuth";

// Chamadas à API
import getCurrentUser from "@/api/getCurrentUser";

interface Options {
  loadOnStartup?: boolean
}

export default function useUserData({ loadOnStartup = false }: Options = {}) {
  const { token } = useAuth()
  const userData = ref<CurrentUserInfo | null>(null)
  const loadingError = ref<string | null>(null)

  async function loadUserData() {
    if (!token.value) return
    try {
      userData.value = await getCurrentUser(token.value)
    } catch (e) {
      loadingError.value = e instanceof Error
        ? e.message
        : 'Erro desconhecido.'
    }
  }

  const nickname = computed(() => userData.value?.nickname)

  if (loadOnStartup) {
    loadUserData()
  }

  return { loadUserData, loadingError, userData, nickname }
}

