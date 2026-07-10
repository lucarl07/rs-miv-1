import formatAPIErrors from "@/utils/formatAPIErrors"

const API_URL = import.meta.env.VITE_API_URL

async function loginAsUser(
  { email, password }: LoginPayload
): Promise<LoginResponse> {

  const res = await fetch(`${API_URL}/auth/login`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ email, password })
  })

  if (!res.ok) {
    const err = await res.json()
    throw new Error(
      err.detail
      ? formatAPIErrors(err.detail)
      : 'Credenciais inválidas.'
    )
  }

  const data: LoginResponse = await res.json()
  return data;
}

export default loginAsUser;
