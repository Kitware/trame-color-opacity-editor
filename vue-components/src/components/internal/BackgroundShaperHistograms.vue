<script setup lang="ts">
import type { Vector2D, OpacityNode } from '@/types';
import { defineProps, computed } from 'vue'

const props = defineProps<{
    nodes: OpacityNode[];
}>();

defineSlots<{
    default(props: {
        shape: Vector2D[];
    }): void;
}>();

const shape = computed(() => {
    const shape: OpacityNode[] = [];

    const empty = props.nodes.length == 0;
    let startX = 0;
    let endX = 1;

    if (!empty) {
        startX = props.nodes[0]![0];
        endX = props.nodes[props.nodes.length - 1]![0];
    }

    shape.push([0, 0])
    shape.push([startX, 0])

    for (let i = 0; i < props.nodes.length - 1; i++) {
        const x = props.nodes[i]![0];
        const y = props.nodes[i]![1];
        const nextX = props.nodes[i + 1]![0];
        shape.push([x, y]);
        shape.push([nextX, y]);
    }

    shape.push([endX, 0])
    shape.push([1, 0])

    return shape;
});

</script>

<template>
    <slot
        :shape
    ></slot>
</template>

<style scoped>
</style>
