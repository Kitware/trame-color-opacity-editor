<script setup lang="ts">
import { defineProps, onMounted, onBeforeUnmount, useTemplateRef, ref, type Ref } from 'vue'

import type { Vector2D } from '@/types'

const props = defineProps<{
}>();

const divEl = useTemplateRef<HTMLDivElement>("div-root");

const viewportSize: Ref<Vector2D> = ref([1, 1]);

let resizeObserver: ResizeObserver | null = null;

onMounted(() => {
  resizeObserver = new ResizeObserver(() => {
    if (divEl.value) {
      const newviewportSize: Vector2D = [divEl.value.clientWidth, divEl.value.clientHeight];
      if ((newviewportSize[0] != viewportSize.value[0]) || (newviewportSize[1] != viewportSize.value[1])) {
        // setTimeout avoids "error: ResizeObserver loop completed with undelivered notifications"
        setTimeout(() => {
          viewportSize.value = newviewportSize;
        }, 0);
      }
    }
  });

  if (divEl.value) {
    resizeObserver.observe(divEl.value);
  }
});

onBeforeUnmount(() => {
  if (resizeObserver) {
    resizeObserver.disconnect();
  }
});
</script>

<template>
    <div ref="div-root">
        <slot
            :viewportSize
        ></slot>
    </div>
</template>

<style scoped>
</style>
