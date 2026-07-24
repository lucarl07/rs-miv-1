import DOMPurify from "dompurify"
import type { Config } from "dompurify"

const SanitizationConfig: Config = {
  /* Apenas overwrites; os métodos já cuidam dos padrões. */
  USE_PROFILES: {
    html: true // Mantêm apenas as tags HTML utilizadas em rich text
  }
}

export async function encryptMessage(
  plaintext: string, key: Uint8Array<ArrayBufferLike>
): Promise<string> {
  const cryptoKey = await crypto.subtle.importKey(
    'raw', key as BufferSource, 'AES-GCM', false, ['encrypt']
  )
  const iv = crypto.getRandomValues(new Uint8Array(12))

  const ciphertext = await crypto.subtle.encrypt(
    { name: 'AES-GCM', iv },
    cryptoKey,
    new TextEncoder().encode(plaintext)
  )

  // Concatena IV + ciphertext, depois base64 pra viajar como string no JSON
  const combined = new Uint8Array(iv.length + ciphertext.byteLength)
  combined.set(iv, 0)
  combined.set(new Uint8Array(ciphertext), iv.length)

  // Transforma a array de inteiros de 8 bits sem sinal (Uint8Array) em um texto Base64
  return btoa(String.fromCharCode(...combined))
}

export async function decryptMessage(
  encoded: string, key: Uint8Array<ArrayBufferLike>
): Promise<string> {
  const cryptoKey = await crypto.subtle.importKey(
    'raw', key as BufferSource, 'AES-GCM', false, ['decrypt']
  )
  // - Itera sob atob(encoded) para transformar cada 'byte-char' em número
  // - Junta todos os números em uma Uint8Array
  const combined = Uint8Array.from(atob(encoded), c => c.charCodeAt(0))

  // Separa o IV presente nos primeiros 12 caracteres do ciphertext
  const iv = combined.slice(0, 12)
  const ciphertext = combined.slice(12)

  const plaintext = await crypto.subtle.decrypt(
    { name: 'AES-GCM', iv },
    cryptoKey,
    ciphertext
  )
  const decoded = new TextDecoder().decode(plaintext)

  return DOMPurify.sanitize(decoded, SanitizationConfig)
}

