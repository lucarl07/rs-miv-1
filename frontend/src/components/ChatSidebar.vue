<script setup lang="ts">
  import { computed } from 'vue'

  const props = defineProps<{
    nickname?: string
    status: string
    userList: string[]
  }>();

  const isNicknameLoaded = computed<boolean>(() => !!props.nickname)
</script>

<template>
  <aside class="flex flex-col px-6 py-4 gap-4">
    <header class="flex flex-row justify-between items-center">
      <hgroup>
        <h2 v-if="isNicknameLoaded" class="text-lg">{{nickname}}</h2>
        <h2 v-else class="text-lg text-gray-400">Carregando...</h2> <!-- TODO: Trocar esse <h2> por uma <div> -->
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
    <ul>
      <li v-for="(user, index) in userList" :key="index">
        {{user}}
      </li>
    </ul>
    <hr class="text-crushed-berry" />
    <!-- Ainda vou ver o que faço com isso aqui ↓ -->
    <a href="https://www.flaticon.com/free-icons/leave" title="leave icons">
      Leave icons created by meaicon - Flaticon
    </a>
  </aside>
</template>
