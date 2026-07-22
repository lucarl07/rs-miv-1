<script setup lang="ts">
  import { computed } from 'vue'

  defineOptions({
    inheritAttrs: false
  })

  const model = defineModel()
  const {
    fieldname, labelText, showOnError, isRequired = true
  } = defineProps<{
    fieldname: string
    labelText?: string
    showOnError?: string
    isRequired?: boolean
  }>()

  const labelTitle = computed<string>(() =>
    isRequired
    ? 'Este campo é obrigatório.'
    : 'Este campo é opcional.'
  )
</script>

<template>
  <div :id="'wrapper_' + fieldname">
    <label
      v-if="labelText"
      :for="fieldname"
      :title="labelTitle"
      class="block text-sm font-medium text-grey-100"
    >
      {{ labelText }}
      <span v-if="isRequired" class="text-red-400">*</span>
    </label>
    <!-- Atributos de passagem serão herdados no input abaixo: -->
    <input
      v-model="model"
      v-bind="$attrs"
      :id="fieldname"
      :required="isRequired"
      :autocomplete="$attrs.autocomplete || fieldname"
      class="
        mt-1.5 px-3 py-2 w-full rounded-md border border-mauve-500
        bg-pale-silver
        focus:outline-double focus:outline-crushed-berry
      "
    />
    <slot name="customBottomText">
      <p
        v-if="showOnError"
        class="mt-1.5 text-sm text-red-400"
      >
        {{ showOnError }}
      </p>
    </slot>
  </div>
</template>

