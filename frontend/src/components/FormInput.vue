<script setup lang="ts">
  import { computed, ref, useAttrs } from 'vue'
  import Icon_HidePassword from '@/assets/icons/HidePassword.vue'
  import Icon_ShowPassword from '@/assets/icons/ShowPassword.vue'

  defineOptions({
    inheritAttrs: false
  })

  const model = defineModel()
  const attrs = useAttrs()
  const {
    fieldname, autocomplete, labelText, showOnError, isRequired = true
  } = defineProps<{
    fieldname: string
    autocomplete?: string
    labelText?: string
    showOnError?: string | null
    isRequired?: boolean
  }>()

  const labelTitle = computed<string>(() =>
    isRequired
    ? 'Este campo é obrigatório.'
    : 'Este campo é opcional.'
  )

  const isPasswordField = computed(() =>
    attrs.type === 'password' || fieldname === 'password'
  )
  const showPassword = ref(false)

  const inputType = computed(() =>
    isPasswordField.value
      ? (showPassword.value ? 'text' : 'password')
      : (attrs.type as string | undefined)
  )

  const passthroughAttrs = computed(() => {
    // Função para retirar os atributos que são dinamicamente manipulados
    // neste componente.
    const { type, ...rest } = attrs
    return rest
  })
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

    <div class="relative mt-1.5">
      <input
        v-model="model"
        v-bind="passthroughAttrs"
        :type="inputType"
        :id="fieldname"
        :required="isRequired"
        :autocomplete="autocomplete || fieldname"
        class="
          px-3 py-2 w-full rounded-md border border-mauve-500
          bg-pale-silver text-crushed-berry
          focus:outline-double focus:outline-crushed-berry
        "
        :class="isPasswordField ? 'pe-10' : ''"
      />
      <button
        v-if="isPasswordField"
        type="button"
        tabindex="-1"
        @click="showPassword = !showPassword"
        :aria-label="showPassword ? 'Ocultar senha' : 'Mostrar senha'"
        class="
          absolute right-2 top-1/2 -translate-y-1/2
          text-mauve-500 hover:text-crushed-berry hover:cursor-pointer
        "
      >
        <Icon_HidePassword v-if="showPassword" class="w-5 h-5" />
        <Icon_ShowPassword v-else class="w-5 h-5" />
      </button>
    </div>

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

