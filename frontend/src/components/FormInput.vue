<script setup lang="ts">
  defineOptions({
    inheritAttrs: false
  })

  const model = defineModel()
  const props = defineProps<{
    fieldname: string
    labelText?: string
    showOnError?: string
  }>()
</script>

<template>
  <div :id="'wrapper_' + fieldname">
    <label
      v-if="labelText"
      :for="fieldname"
      class="block text-sm font-medium text-grey-100"
    >
      {{ labelText }}
    </label>
    <!-- Atributos de passagem serão herdados no input abaixo: -->
    <input
      v-model="model"
      v-bind="$attrs"
      :id="fieldname"
      class="
        mt-1.5 px-3 py-2 w-full rounded-md border border-mauve-500
        bg-pale-silver
        focus:outline-double focus:outline-crushed-berry
      "
    />
    <slot name="customBottomText">
      <p
        v-if="showOnError"
        class="mt-1.5 text-sm"
      >
        {{ showOnError }}
      </p>
    </slot>
  </div>
</template>

