const timeOptions: {
  hour?: '2-digit' | 'numeric'
  minute?: '2-digit' | 'numeric'
} = {
  hour: '2-digit',
  minute: '2-digit'
}

const formatters = {
  overAYearAgo: new Intl.DateTimeFormat('pt-BR', {
    day: '2-digit',
    month: '2-digit',
    year: 'numeric',
    ...timeOptions
  }),
  overAWeekAgo: new Intl.DateTimeFormat('pt-BR', {
    day: 'numeric',
    month: 'long',
    ...timeOptions
  }),
  overADayAgo: new Intl.DateTimeFormat('pt-BR', {
    weekday: 'long',
    ...timeOptions
  }),
  todayOrYesterday: new Intl.DateTimeFormat('pt-BR', timeOptions)
}

/** Essa função deve retornar os seguintes resultados:
 * ===================================================
 * 00/00/0000, 00:00    | mais de um ano atrás
 * 1 de abril, 00:00	  | mais de uma semana atrás
 * segunda-feira, 00:00 | mais de um dia atrás
 * ontem, 00:00		      | um dia atrás
 * 00:00				        | um dia atrás
 * ===================================================
 */
export default function formatDate(date: Date): string {
  const now: Date = new Date()

  // Normaliza 'now' e 'date' para meia-noite
  const today = new Date(now.getFullYear(), now.getMonth(), now.getDate())
  const msgDay = new Date(date.getFullYear(), date.getMonth(), date.getDate())

  // Comparando os dias de calendário 'today' e 'msgDay' pelo número de milissegundos em um dia
  const diffDays = Math.floor(
    (today.getTime() - msgDay.getTime()) / 86_400_000
  )

  // Obtendo a formatação que deve ser utilizada, com base no tamanho da diferença das datas em dias
  if (diffDays > 365) return formatters.overAYearAgo.format(date)
  if (diffDays > 7)   return formatters.overAWeekAgo.format(date)
  if (diffDays > 1)   return formatters.overADayAgo.format(date)
  if (diffDays === 1) return `ontem, ${formatters.todayOrYesterday.format(date)}`
  return formatters.todayOrYesterday.format(date)
}
