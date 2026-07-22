<script setup lang="ts">
  import { ref } from 'vue'
  import { useRouter } from 'vue-router'
  import useAuth from '@/composables/useAuth'
  import FormInput from '@/components/FormInput.vue'

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

    <div
      v-if="errorMessage"
      class="text-center text-sm text-red-400"
    >
      <p class="font-bold">Erro ao tentar fazer login:</p>
      <p>{{ errorMessage }}</p>
    </div>
    <p class="text-center text-mauve-400">
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
