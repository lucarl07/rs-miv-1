<script setup lang="ts">
  import { ref } from 'vue'
  import { useRouter } from 'vue-router'
  import useAuth from '@/composables/useAuth'

  const router = useRouter()
  const { register } = useAuth()

  const nickname = ref('')
  const email = ref('')
  const password = ref('')
  const confirmPassword = ref('')
  const errorMessage = ref<SignupFormErrors>({
    email: null, password: null,
    confirmPassword: null, other: null
  })
  const isSubmitting = ref(false)

  async function handleSubmit(): Promise<void> {
    for (const key in errorMessage.value) {
      errorMessage.value[key as keyof SignupFormErrors] = null
    }

    if (password.value !== confirmPassword.value) {
      errorMessage.value.confirmPassword = 'As senhas não coincidem.'
      return
    }

    isSubmitting.value = true

    try {
      await register(nickname.value, email.value, password.value)
      router.push({ name: 'login' })
    } catch (err) {
      errorMessage.value.other = err instanceof Error
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
          mt-1 px-3 py-2 w-full rounded-md border border-mauve-500
          bg-pale-silver
          focus:outline-double focus:outline-crushed-berry
        "
      />
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
          mt-1 px-3 py-2 w-full rounded-md border border-mauve-500
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
          mt-1 px-3 py-2 w-full rounded-md border border-mauve-500
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
          mt-1 px-3 py-2 w-full rounded-md border border-mauve-500
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
