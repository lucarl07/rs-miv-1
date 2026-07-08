// Dependências Externas
import { ref, computed } from "vue";

// Chamadas à API
import getCurrentUser from "@/api/getCurrentUser";

const TOKEN_KEY = 'access_token'
const token = ref<string | null>(sessionStorage.getItem(TOKEN_KEY))

interface Options {
  loadOnStartup?: boolean
}

export default function useUserData({ loadOnStartup = false }: Options) {
  const userData = ref<CurrentUserInfo | null>(null)

  async function loadUserData() {
    userData.value = await getCurrentUser(token.value)
  }

  const nickname = computed(() => userData.value?.nickname)

  if (loadOnStartup) {
    loadUserData()
  }

  return { loadUserData, userData, nickname }
}
