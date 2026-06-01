<script setup lang="ts">
  const props = defineProps<{
    username: String,
    content: String,
    timestamp: String,
    isSystemMessage: { type: Boolean }
  }>();

  // Date of the sent message
  const typedDate: Date = new Date('2020-01-24')
  const currentDate: Date = new Date()
  // const sentAt: String = typedDate.toLocaleString('pt-BR');

  let sentAt: String

  if (typedDate.getFullYear() < currentDate.getFullYear()) {
    sentAt = `${typedDate.getDate() + 1} de ${typedDate.getMonth() + 1}`
  } else {
    sentAt = typedDate.toLocaleString('pt-BR');
  }

  const sysMsgClasses = props.isSystemMessage
    ? 'italic text-[#956f81]'
    : ''
</script>

<template>
  <article class="mb-6">
    <header class="flex gap-2">
      <span
        id="message_username"
        :class="['font-bold', sysMsgClasses]"
      >
        {{username}}
      </span>
      <span
        id="message_sentAt"
        class="font-medium text-grey-500"
      >
        {{sentAt}}
      </span>
    </header>
    <span id="message_content">
      {{content}}
    </span>
  </article>
</template>

