import { ref } from 'vue'

const sessionKey = ref<PGPSessionKey>(null)

export function useSessionKey() {
  function setSessionKey(key: Uint8Array) {
    sessionKey.value = key
  }

  function getSessionKey(): PGPSessionKey {
    return sessionKey.value
  }

  return { sessionKey, setSessionKey, getSessionKey }
}
