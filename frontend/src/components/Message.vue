<script setup lang="ts">
  import formatDate from '../utils/formatDate.ts'

  const props = defineProps<{
    username: string,
    content: string,
    timestamp: string,
    isSystemMessage?: boolean
  }>();

  const typedDate: Date = new Date(props.timestamp)
  const sentAt = formatDate(typedDate)

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

