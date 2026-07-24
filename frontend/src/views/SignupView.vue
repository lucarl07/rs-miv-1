<script setup lang="ts">
  import { ref, watch, computed } from 'vue'
  import { useRouter } from 'vue-router'

  import checkNicknameAvailability from '@/api/checkNicknameAvailability'
  import useAuth from '@/composables/useAuth'
  import {
    NICKNAME_REGEX,
    checkEmailValidity, checkPasswordValidity, checkPasswordsMatch
  } from '@/utils/signUpValidation'

  import Button from '@/components/Button.vue'
  import FormInput from '@/components/FormInput.vue'
  import ErrorMessage from '@/components/ErrorMessage.vue'

  const router = useRouter()
  const { register } = useAuth()

  const nickname = ref('')
  const email = ref('')
  const password = ref('')
  const confirmPassword = ref('')
  const isSubmitting = ref(false)

  const nicknameStatus = ref<AsyncFieldEvalStatus>('idle')
  const nicknameStatusMessage = computed(() => {
    switch (nicknameStatus.value) {
      case 'checking':
        return 'Verificando disponibilidade...'
      case 'available':
        return 'Nickname disponível!'
      case 'taken':
        return 'Esse nickname já está em uso'
      case 'invalid':
        return 'Use de 5 a 30 caracteres (letras, números, _ ou -)'
      default:
        return null
    }
  })
  const nicknameStatusClass = computed(() => {
    switch (nicknameStatus.value) {
      case 'checking':
        return 'text-gray-400'
      case 'available':
        return 'text-green-600'
      case 'taken': case 'invalid':
        return 'text-red-400'
      default:
        return ''
    }
  })

  const errorMessages = computed<SignupFormErrors>(() => ({
    nickname: nicknameStatusMessage.value,
    email: checkEmailValidity(email.value),
    password: checkPasswordValidity(password.value),
    confirmPassword: checkPasswordsMatch(
      password.value, confirmPassword.value
    )
  }))
  const backendErrorMessage = ref<string | null>(null)

  let debounceTimer: ReturnType<typeof setTimeout> | null = null
  let checkController: AbortController | null = null

  function clearDebounce() {
    if (debounceTimer !== null) {
      clearTimeout(debounceTimer)
      debounceTimer = null
    }
  }

  async function triggerNicknameCheck(value: string) {
    checkController?.abort()
    checkController = new AbortController()

    nicknameStatus.value = 'checking'

    try {
      const result = await checkNicknameAvailability(value, checkController.signal)
      nicknameStatus.value = result?.available ? 'available' : 'taken'
    } catch (err) {
      if (err instanceof DOMException && err.name === 'AbortError') return
      nicknameStatus.value = 'idle'
    }
  }

  watch(nickname, (newValue) => {
    clearDebounce()
    const trimmed = newValue.trim()

    // 1. Verifica se há algum texto no input
    if (trimmed.length === 0) {
      nicknameStatus.value = 'idle'
      return
    }

    // 2. Aguarda 500 milissegundos (ms)
    debounceTimer = setTimeout(() => {
      // 3. SE trimmed É INVÁLIDO:
      if (!NICKNAME_REGEX.test(trimmed)) {
        nicknameStatus.value = 'invalid'
        return
      }
      // 3. SE NÃO:
      triggerNicknameCheck(trimmed)
    }, 500)
  })

  const isFormValid = computed<boolean>(() => {
    const allFieldsFilled =
      nicknameStatus.value === 'available' &&
      // ↑ Além de preenchido, garante que ele está disponível
      email.value.trim().length > 0 &&
      password.value.length > 0 &&
      confirmPassword.value.length > 0

    const noErrors =
      errorMessages.value.email === null &&
      errorMessages.value.password === null &&
      errorMessages.value.confirmPassword === null

    return allFieldsFilled && noErrors
  })

  async function handleSubmit(): Promise<void> {
    for (const key in errorMessages.value) {
      errorMessages.value[key as keyof SignupFormErrors] = null
    }

    if (password.value !== confirmPassword.value) {
      errorMessages.value.confirmPassword = 'As senhas não coincidem.'
      return
    }

    isSubmitting.value = true

    try {
      await register(nickname.value, email.value, password.value)
      router.push({ name: 'login' })
    } catch (err) {
      backendErrorMessage.value = err instanceof Error
        ? err.message
        : 'Erro inesperado ao tentar criar conta.'
    } finally {
      isSubmitting.value = false
    }
  }
  function handleGoToLogin(): void {
    router.push({ name: 'login' })
  }
</script>

<template>
  <main class="flex flex-col flex-1 items-center py-page-y">
    <h1 class="w-lg text-4xl text-center font-semibold">
      Crie uma conta para não ficar de fora!
    </h1>
    <div class="flex flex-1 items-center justify-center">
      <form class="grid grid-cols-2 gap-4 w-xl" @submit.prevent="handleSubmit">
        <FormInput
          v-model="nickname"
          fieldname="nickname"
          labelText="Nome de usuário"
          type="text"
        >
          <template #customBottomText>
            <p
              v-if="errorMessages.nickname"
              class="mt-1.5 text-sm"
              :class="nicknameStatusClass"
            >
              {{ errorMessages.nickname }}
            </p>
          </template>
        </FormInput>

        <FormInput
          v-model="email"
          fieldname="email"
          labelText="E-mail"
          type="email"
          :showOnError="errorMessages.email"
        />

        <FormInput
          v-model="password"
          fieldname="password"
          labelText="Senha"
          autocomplete="new-password"
          type="password"
          :showOnError="errorMessages.password"
        />

        <div
          id="wrapper_about_password"
          class="
            flex flex-col justify-evenly p-2 row-span-2
            border border-white rounded-md text-sm
          "
        >
          <h3 class="font-semibold">A senha deve conter, no mínimo:</h3>
          <ul class="list-inside list-disc">
            <li>Tamanho de 8 caracteres</li>
            <li>Um número</li>
            <li>Uma letra maiúscula</li>
            <li>Uma letra minúscula</li>
            <li>Um caractere especial</li>
          </ul>
        </div>

        <FormInput
          v-model="confirmPassword"
          fieldname="confirm-password"
          labelText="Confirmar senha"
          autocomplete="new-password"
          type="password"
          :showOnError="errorMessages.confirmPassword"
        />


        <div id="wrapper_buttons" class="col-span-2 flex h-12 gap-4">
          <Button
            type="submit"
            :disabled="!isFormValid"
            :title="!isFormValid && 'Preencha corretamente todos os campos.'"
            class="bg-crushed-berry w-1/2"
            text="Criar conta"
          />
          <Button
            @click="handleGoToLogin"
            class="bg-gray-500 w-1/2"
            text="Já tenho uma conta"
          />
        </div>

        <ErrorMessage
          v-if="backendErrorMessage"
          error-type="Erro pós-envio"
          :message="backendErrorMessage"
          class="col-span-2"
        />
      </form>
    </div>
  </main>
</template>
