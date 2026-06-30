<script setup lang="ts">
  import { ref } from 'vue'
  import { useRouter } from 'vue-router'
  import useAuth from '@/composables/useAuth'

  const router = useRouter()
  const { login } = useAuth()

  const email = ref('')
  const password = ref('')
  const errorMessage = ref<string | null>(null)
  const isSubmitting = ref(false)

  async function handleSubmit(): Promise<void> {
    errorMessage.value = null
    isSubmitting.value = true

    try {
      await login(email.value, password.value)
      router.push({ name: 'chat' })
    } catch (err) {
      errorMessage.value = err instanceof Error
        ? err.message
        : 'Erro inesperado ao tentar entrar.'
    } finally {
      isSubmitting.value = false
    }
  }

  function handleRegister(): void {
    // TODO: Criar página 'register'
    // router.push({ name: 'register' })
    console.log('[T.B.D]')
  }
</script>

<template>
  <form @submit.prevent="handleSubmit" class="flex flex-col gap-4 w-sm">
    <div>
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

    <div>
      <label for="password" class="block text-sm font-medium text-grey-100">
        Senha
      </label>
      <input
        id="password"
        v-model="password"
        type="password"
        required
        autocomplete="current-password"
        class="
          mt-1 px-3 py-2 w-full rounded-md border border-mauve-500
          bg-pale-silver
          focus:outline-double focus:outline-crushed-berry
        "
      />
    </div>

    <p v-if="errorMessage" class="text-sm text-red-600">
      {{ errorMessage }}
    </p>

    <button
      type="submit"
      :disabled="isSubmitting"
      class="
        px-4 py-2 rounded-md bg-crushed-berry text-white
        disabled:opacity-50 hover:cursor-pointer
      "
    >
      {{ isSubmitting ? 'Entrando...' : 'Entrar' }}
    </button>

    <p class="text-mauve-400">
      Ainda não tem uma conta?
      <span
        @click="handleRegister"
        class="text-blue-400 hover:underline hover:cursor-pointer"
      >
        Cadastre-se
      </span>
    </p>
  </form>
</template>
