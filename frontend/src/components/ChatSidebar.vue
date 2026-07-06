<script setup lang="ts">
  const props = defineProps<{
    nickname: string
    status: string
  }>();
</script>

<template>
  <aside class="flex flex-col px-6 py-4 gap-4">
    <header class="flex flex-row justify-between items-center">
      <hgroup>
        <h2 class="text-lg">{{nickname}}</h2>
        <p class="text-sm">
          <span class="font-bold">Status:</span>
          {{status}}
        </p>
      </hgroup>
      <div id="btn_wrapper">
        <slot name="options" />
      </div>
    </header>
    <hr class="text-crushed-berry" />
    <a href="https://www.flaticon.com/free-icons/leave" title="leave icons">Leave icons created by meaicon - Flaticon</a>
  </aside>
</template>
