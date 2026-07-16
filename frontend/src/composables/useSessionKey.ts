import { ref } from 'vue'

const sessionKey = ref<PGPSessionKey>(null)

let resolveKeyReady: (key: Uint8Array) => void
const sessionKeyReady = new Promise<Uint8Array>(resolve => {
  resolveKeyReady = resolve
})

export function useSessionKey() {
  function setSessionKey(key: Uint8Array) {
    sessionKey.value = key
    resolveKeyReady(key)
  }

  function getSessionKey(): PGPSessionKey {
    return sessionKey.value
  }

  function waitForSessionKey(): Promise<Uint8Array> {
    return sessionKeyReady
  }

  return { sessionKey, setSessionKey, getSessionKey, waitForSessionKey }
}
