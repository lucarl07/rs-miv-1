<script setup lang="ts">
  import LoginForm from '@/components/LoginForm.vue'
</script>

<template>
  <main class="flex flex-col flex-1 items-center py-page-y">
    <h1 class="w-lg text-4xl text-center font-semibold">
      Entre na sua conta e se divirta com os seus amigos!
    </h1>
    <div class="flex flex-1 items-center justify-center">
      <LoginForm />
    </div>
  </main>
</template>
