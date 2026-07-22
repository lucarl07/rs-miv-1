export const NICKNAME_REGEX = /^[a-zA-Z0-9_-]{5,30}$/

export const EMAIL_REGEX = /^[^\s@]+@[^\s@]+\.[^\s@]+$/

export const PASSWORD_REGEX = /^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[^a-zA-Z\d]).{8,}$/

export function checkEmailValidity(email: string): string | null {
  if (email.trim().length === 0) return null // Campo vazio não é "erro" ainda
  if (!EMAIL_REGEX.test(email)) return 'Formato de email inválido'
  return null
}

export function checkPasswordValidity(password: string): string | null {
  if (password.length === 0) return null
  if (!PASSWORD_REGEX.test(password)) {
    return 'A senha precisa ter ao menos 8 caracteres, com maiúscula, minúscula, número e caractere especial'
  }
  return null
}

export function checkPasswordsMatch(password: string, confirmPassword: string): string | null {
  if (confirmPassword.length === 0) return null
  if (password !== confirmPassword) return 'As senhas não coincidem'
  return null
}
