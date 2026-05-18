<script setup lang="ts">
  import { ref } from 'vue'

  const emit = defineEmits(['send'])

  const message = ref('')

  function handleSubmit() {
    emit('send', message.value)
    message.value = ''
  }
</script>

<template>
  <form @submit.prevent>
    <input type="text" v-model="message" />
    <button @click="handleSubmit">
      Enviar
    </button>
  </form>
</template>
