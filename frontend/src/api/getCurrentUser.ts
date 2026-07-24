import formatAPIErrors from "@/utils/formatAPIErrors"

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
      err.detail
      ? formatAPIErrors(err.detail)
      : 'Erro ao buscar o usuário atual.'
    )
  }

  const data = await res.json()
  return data;
}

export default getCurrentUser;
