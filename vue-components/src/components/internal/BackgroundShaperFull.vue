<script setup lang="ts">
import type { Vector2D } from '@/types';

defineSlots<{
    default(props: {
        shape: Vector2D[];
    }): void;
}>();

</script>

<template>
    <slot
        :shape="[
            [0, 0],
            [1, 0],
            [1, 1],
            [0, 1],
        ]"
    ></slot>
</template>

<style scoped>
</style>
