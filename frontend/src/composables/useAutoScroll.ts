import { ref, onMounted, watch, nextTick } from 'vue'

type ShouldScrollCallback = (newItems: any[]) => boolean

export default function useAutoScroll(
  items: any[], shouldScroll: ShouldScrollCallback
) {
  const scrollTarget = ref<HTMLElement | null>(null)

  function scrollToBottom() {
    if (scrollTarget.value) {
      scrollTarget.value.scrollTop = scrollTarget.value.scrollHeight
    }
  }

  onMounted(() => {
    scrollToBottom()
  })

  watch(items, (newItems) => {
    if (shouldScroll(newItems)) {
      nextTick(() => scrollToBottom())
    }
  })

  return { scrollTarget, scrollToBottom }
}
