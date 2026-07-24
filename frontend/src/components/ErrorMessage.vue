<template>
  <div class="text-center text-sm text-red-400">
    <p v-if="inlineMessage">
      <span class="font-bold">{{ errorType }}:</span>
      {{ message }}
    </p>
    <template v-else>
      <p class="font-bold">{{ errorType }}:</p>
      <p>{{ message }}</p>
    </template>
  </div>
  <!-- NOTA:
    A condição escolhida para o erro aparecer fica a critério do
    componente pai.
  -->
</template>

<script setup lang="ts">
  const {
    errorType = 'Erro',
    message,
    inlineMessage = true,
  } = defineProps<{
    errorType?: string
    message: string
    inlineMessage?: boolean
  }>()
</script>
