<script setup lang="ts">
  import RegisterForm from '@/components/RegisterForm.vue'
</script>

<template>
  <main class="flex flex-col flex-1 items-center py-page-y">
    <h1 class="w-lg text-4xl text-center font-semibold">
      Crie uma conta para não ficar de fora!
    </h1>
    <div class="flex flex-1 items-center justify-center">
      <RegisterForm />
    </div>
  </main>
</template>
