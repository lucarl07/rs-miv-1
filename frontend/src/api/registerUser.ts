import formatPydanticErrors from "@/utils/formatPydanticErrors"

const API_URL = import.meta.env.VITE_API_URL

/** Para cadastrar usuário:
 * 1 - Receber dados (nickname, email e senha)
 * 2 - Tratar os dados: [deixarei por último, visto que o back-end tem suas próprias validações]
 *    - E-mail: deve seguir as normas básicas de um e-mail.
 *    - Senha: Deve conter no mínimo 8 caracteres, dentre eles ao menos uma letra maiúscula, uma
 *    letra minúscula, um número e um caractere especial.
 * 3 - Mandar para a API;
 * 4 - Tratar resposta da API:
 *    - Caso mal sucedido: exibir erro (ex. e-mail não único, nickname não único, erro interno do
 *    servidor)
 *    - Caso bem sucedido: redirecionar para a página de login.
 */

async function registerUser(
  { nickname, email, password }: RegisterUserPayload
): RegisterUserResponse {

  const res = await fetch(`${API_URL}/auth/register`, {
    method: 'POST',
    headers: { "Content-Type": "application/json", },
    body: JSON.stringify({ nickname, email, password }),
  })

  if (!res.ok) {
    const err = await res.json()
    throw new Error(
      err.detail ??                       // Caso err.detail seja uma string simples
      formatPydanticErrors(err.detail) ?? // Caso err.detail seja um retorno (objeto) do Pydantic
      'Erro no cadastro.'                 // Caso err.detail seja outro formato
    )
  }
}

export default registerUser;
