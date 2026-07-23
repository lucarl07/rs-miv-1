<script setup lang="ts">
  import { ref } from 'vue'
  import { useRouter } from 'vue-router'
  import useAuth from '@/composables/useAuth'
  import FormInput from '@/components/FormInput.vue'
  import ErrorMessage from '@/components/ErrorMessage.vue'

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
    router.push({ name: 'signup' })
  }
</script>

<template>
  <main class="flex flex-col flex-1 items-center py-page-y">
    <h1 class="w-lg text-4xl text-center font-semibold">
      Entre na sua conta e se divirta com os seus amigos!
    </h1>
    <div class="flex flex-1 items-center justify-center">
      <form @submit.prevent="handleSubmit" class="flex flex-col gap-4 w-sm">
        <FormInput
          v-model="email"
          fieldname="email"
          label-text="E-mail"
          type="email"
        />
        <FormInput
          v-model="password"
          fieldname="password"
          label-text="Senha"
          autocomplete="current-password"
        />

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

        <ErrorMessage
          v-if="errorMessage"
          error-type="Erro ao tentar fazer login"
          :message="errorMessage"
          :inline-message="false"
        />

        <p class="text-center text-sm text-mauve-400">
          Ainda não tem uma conta?
          <span
            @click="handleRegister"
            class="text-blue-400 hover:underline hover:cursor-pointer"
          >
            Cadastre-se
          </span>
        </p>
      </form>
    </div>
  </main>
</template>
