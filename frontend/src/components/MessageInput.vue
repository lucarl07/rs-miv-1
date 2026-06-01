<script setup lang="ts">
  import { ref } from 'vue'

  import icon_btnSend from '../assets/icons/btn_send.svg'

  const emit = defineEmits(['send'])

  const message = ref('')

  function triggerSendEmit() {
    if (message.value.length > 0) {
      emit('send', message.value)
    }
    message.value = ''
  }

  const handleKeyDown = (event) => {
    if (event.key === "Enter" && !event.altKey && !event.shiftKey) {
      event.preventDefault()
      triggerSendEmit()
    }
  }
  const handleSubmit = () => {
    triggerSendEmit()
  }
</script>

<template>
  <form @submit.prevent
    class="
      flex h-10 rounded-sm bg-pale-silver
      focus-within:outline-crushed-berry focus-within:outline-double
    "
  >
    <textarea
      v-model="message"
      @keydown="handleKeyDown"
      autofocus="true"
      spellcheck="true"
      minlength="1"
      maxlength="2000"
      class="
        w-full h-full resize-none px-4 py-2 text-crushed-berry
        focus:outline-none
      "
    />
    <button @click="handleSubmit" type="submit" class="px-4">
      <img
        :src="icon_btnSend"
        alt="Botão de enviar"
        class="w-7 h-7"
      />
    </button>
  </form>
</template>
