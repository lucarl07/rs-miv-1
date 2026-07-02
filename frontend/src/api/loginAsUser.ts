import formatPydanticErrors from "@/utils/formatPydanticErrors"

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
      err.detail ??                       // Caso err.detail seja uma string simples
      formatPydanticErrors(err.detail) ?? // Caso err.detail seja um retorno (objeto) do Pydantic
      'Credenciais inválidas.'            // Caso err.detail seja outro formato
    )
  }

  const data: LoginResponse = await res.json()
  return data;
}

export default loginAsUser;
