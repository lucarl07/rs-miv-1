export default function formatPydanticErrors(errors: any[]): string {
  let strErrors = ''
  let len = errors.length

  if (len < 2) {
    strErrors = errors[0].msg
    return strErrors;
  }

  for (let i = 0; i < len; i++) {
    if (i !== len - 1) {
      strErrors += `${i+1}. ${errors[i].msg};\n`
    } else {
      strErrors += `${i+1}. ${errors[i].msg}.\n`
    }
  }

  return strErrors
}
