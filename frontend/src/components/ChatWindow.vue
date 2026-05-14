<script setup lang="ts">
  import Message from "./Message.vue"

  const messages = [
    // Array demonstrativa apenas; O template usará os dados recebidos pela API.
    {
      id: '10aec4a9-805b-456d-9bf2-2807aec1e783',
      nickname: 'Fulano de Tal',
      content: "Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry's standard dummy text ever since the 1500s, when an unknown printer took a galley of type and scrambled it to make a type specimen book.",
      timestamp: new Date().toISOString()
    },
  ]

  console.log(messages[0])
</script>

<template>
  <main>
    <ol>
      <li v-for="(message, index) in messages" :key="message.id">
        <Message
          :username="message.nickname"
          :content="message.content"
          :timestamp="message.timestamp"
          />
      </li>
    </ol>
  </main>
</template>

