const API_URL = import.meta.env.VITE_API_URL

async function uploadPublicKey(
  token: string | null, public_key: string
): Promise<void> {

  const res = await fetch(`${API_URL}/users/me/public-key`, {
    method: 'POST',
    headers: {
      Authorization: `Bearer ${token}`,
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({ public_key }),
  })

  if (!res.ok) {
    const err = await res.json()
    throw new Error(
      err.detail ??
      'Erro desconhecido ao enviar chave pública do usuário.'
    )
  }
}

export default uploadPublicKey;
