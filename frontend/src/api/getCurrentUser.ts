const API_URL = import.meta.env.VITE_API_URL

async function getCurrentUser(
  token: string | null
): Promise<CurrentUserResponse> {

  const res = await fetch(`${API_URL}/users/me`, {
    headers: { Authorization: `Bearer ${token}` }
  })

  if (!res.ok) {
    const err = await res.json()
    throw new Error(
      err.detail ??                     // Caso err.detail seja uma string simples
      'Erro ao buscar o usuário atual.' // Caso err.detail seja outro formato
    )
  }

  const data = await res.json()
  return data;
}

export default getCurrentUser;
