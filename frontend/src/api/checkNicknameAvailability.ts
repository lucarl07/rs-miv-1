import formatAPIErrors from "@/utils/formatAPIErrors"

const API_URL = import.meta.env.VITE_API_URL

async function checkNicknameAvailability(
  nickname: string,
  signal?: AbortSignal
): Promise<{ available: boolean } | null> {

  const response = await fetch(
    `${API_URL}/users/check-nickname/${nickname}`,
    { method: 'GET', signal }
  )

  if (!response.ok) {
    const errorBody = await response.json();
    throw new Error(errorBody.detail
      ? formatAPIErrors(errorBody.detail)
      : 'Erro inesperado ao averiguar a disponiblidade do nome.'
    )
  }

  return response.json();
}

export default checkNicknameAvailability;
