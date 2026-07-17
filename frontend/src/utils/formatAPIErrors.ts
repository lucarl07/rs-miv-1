interface PydanticError {
  msg: string
  loc: (string | number)[]
  type: string
}

export default function formatAPIErrors(err: string | PydanticError[]): string {
  if (!Array.isArray(err)) {
    return err
  }

  let strErr = ''
  let len = err.length

  if (len === 0) {
    console.error('Aviso sobre a API: Erro não identificado capturado.')
    return 'Erro desconhecido.' // Caso uma array vazia seja encaminhada como erro
  }
  if (len === 1) {
    const error = err[0]

    if (!error) {
      console.error('Aviso sobre a API: Erro não identificado capturado.')
      return 'Erro desconhecido.'
    }

    return error.msg
  }

  for (const [i, error] of err.entries()) {
    if (i !== len - 1) {
      strErr += `${i+1}. ${error.msg};\n`
    } else {
      strErr += `${i+1}. ${error.msg}.\n`
    }
  }

  return strErr
}
