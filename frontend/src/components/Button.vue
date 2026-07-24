<template>
  <button
    type="button"
    class="
      flex rounded-md items-center justify-center
      cursor-pointer disabled:opacity-75
    "
  >
    <slot name="icons" />
    <span>{{ text }}</span>
  </button>
</template>

<script setup lang="ts">
  const props = defineProps<{
    text: string
  }>()
</script>
