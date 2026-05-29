<script setup lang="ts">
  const props = defineProps({
    username: String,
    content: String,
    timestamp: String
  });

  const typedDate: Date = new Date(props.timestamp)
  const sentAt: String = typedDate.toLocaleString("pt-BR");
</script>

<template>
  <article class="mb-6">
    <header class="flex gap-2">
      <span
        id="message_username"
        class="font-bold"
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

