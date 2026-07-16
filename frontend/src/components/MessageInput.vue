<script setup lang="ts">
  import { ref, computed } from 'vue'

  import icon_btnSend from '../assets/icons/btn_send.svg'

  const {
    enableSend = true
  } = defineProps<{
    enableSend: boolean
  }>()
  const emit = defineEmits(['send'])

  const message = ref('')
  const placeholder = computed<string>(() => enableSend
    ? 'Digite qualquer coisa...'
    : 'Aguardando o chat carregar...'
  );

  function triggerSendEmit() {
    if (message.value.length > 0) {
      emit('send', message.value)
    }
    message.value = ''
  }

  function handleKeyDown(event) {
    if (event.key === "Enter" && !event.altKey && !event.shiftKey) {
      event.preventDefault()
      triggerSendEmit()
    }
  }
  function handleSubmit() {
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
      :disabled="!enableSend"
      :placeholder="placeholder"
      autofocus="true"
      spellcheck="true"
      minlength="1"
      maxlength="2000"
      class="
        w-full h-full resize-none px-4 py-2 text-crushed-berry
        focus:outline-none
        peer disabled:italic
      "
    />
    <button
      @click="handleSubmit"
      type="submit"
      class="px-4 peer-disabled:hidden"
    >
      <img
        :src="icon_btnSend"
        alt="Botão de enviar"
        class="w-7 h-7"
      />
    </button>
  </form>
</template>
