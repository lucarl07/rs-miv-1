export default function genUniqueNickname(nickname: string): string {
  const randomHexTag: string = Math.random().toString(16).slice(2, 6);
  const uniqueNickname = `${nickname}.${randomHexTag}`
  return uniqueNickname;
}

