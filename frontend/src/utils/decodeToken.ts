import { jwtDecode } from "jwt-decode";

interface AccessTokenPayload {
  sub: UserId
  exp: number
}

export default function decodeToken(token: string) {
  try {
    return jwtDecode<AccessTokenPayload>(token)
  } catch {
    return null
  }
}

