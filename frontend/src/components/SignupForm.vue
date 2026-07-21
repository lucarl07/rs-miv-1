<script setup lang="ts">
  import { ref, watch, computed } from 'vue'
  import { useRouter } from 'vue-router'

  import checkNicknameAvailability from '@/api/checkNicknameAvailability'
  import useAuth from '@/composables/useAuth'
  import {
    NICKNAME_REGEX,
    checkEmailValidity, checkPasswordValidity, checkPasswordsMatch
  } from '@/utils/signUpValidation.ts'

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
    ),
    other: null
  }))

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
      errorMessages.value.other = err instanceof Error
        ? err.message
        : 'Erro inesperado ao tentar criar conta.'
    } finally {
      isSubmitting.value = false
    }
  }
</script>

<template>
  <form class="grid grid-cols-2 gap-4 w-xl" @submit.prevent="handleSubmit">
    <div id="wrapper_username">
      <label for="nickname" class="block text-sm font-medium text-grey-100">
        Nome de usuário
      </label>
      <input
        id="nickname"
        v-model="nickname"
        type="text"
        required
        autocomplete="nickname"
        class="
          mt-1.5 px-3 py-2 w-full rounded-md border border-mauve-500
          bg-pale-silver
          focus:outline-double focus:outline-crushed-berry
        "
      />
      <p
        v-if="errorMessages.nickname"
        class="mt-1.5 text-sm"
        :class="nicknameStatusClass"
      >
        {{ errorMessages.nickname }}
      </p>
    </div>

    <div id="wrapper_email">
      <label for="email" class="block text-sm font-medium text-grey-100">
        E-mail
      </label>
      <input
        id="email"
        v-model="email"
        type="email"
        required
        autocomplete="email"
        class="
          mt-1.5 px-3 py-2 w-full rounded-md border border-mauve-500
          bg-pale-silver
          focus:outline-double focus:outline-crushed-berry
        "
      />
    </div>

    <div id="wrapper_password">
      <label for="password" class="block text-sm font-medium text-grey-100">
        Senha
      </label>
      <input
        id="password"
        v-model="password"
        type="password"
        required
        autocomplete="new-password"
        class="
          mt-1.5 px-3 py-2 w-full rounded-md border border-mauve-500
          bg-pale-silver
          focus:outline-double focus:outline-crushed-berry
        "
      />
    </div>

    <div
      id="wrapper_about_password"
      class="p-2 max-h-37 border border-white row-span-2 text-sm"
    >
      <h3>A senha deve conter, no mínimo:</h3>
      <ul>
        <li>
          Um número
        </li>
        <li>
          Uma letra maiúscula
        </li>
        <li>
          Uma letra minúscula
        </li>
        <li>
          Um caractere especial
        </li>
        <li>
          Tamanho de 8 caracteres
        </li>
      </ul>
    </div>

    <div id="wrapper_confirm_password">
      <label
        for="confirm_password"
        class="block text-sm font-medium text-grey-100">
        Confirmar senha
      </label>
      <input
        id="confirm_password"
        v-model="confirmPassword"
        type="password"
        required
        autocomplete="confirm_password"
        class="
          mt-1.5 px-3 py-2 w-full rounded-md border border-mauve-500
          bg-pale-silver
          focus:outline-double focus:outline-crushed-berry
        "
      />
    </div>

    <div id="wrapper_buttons" class="col-span-2 flex h-12 gap-4">
      <button type="submit" class="flex w-1/2 bg-crushed-berry items-center justify-center">
        Criar conta
      </button>
      <button type="button" class="flex w-1/2 bg-gray-500 items-center justify-center">
        Já tenho uma conta
      </button>
    </div>
  </form>
</template>
