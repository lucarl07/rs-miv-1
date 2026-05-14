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
  <header>
    <span id="message_username">{{username}}</span>
    <br />
    <span id="message_sentAt">{{sentAt}}</span>
  </header>
  <span id="message_content">
    {{content}}
  </span>
</template>

