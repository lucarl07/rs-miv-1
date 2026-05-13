<script setup lang="ts">
  const props = defineProps({
    user_nickname: String,
    content: String,
    sent_at: Date
  });
</script>

<template>
  <li>
    <figure>
      <figcaption>
        <span>{user_nickname}</span>
      </figcaption>
    </figure>
  </li>
</template>

