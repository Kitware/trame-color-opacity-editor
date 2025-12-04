<script setup lang="ts">
import { defineProps, computed } from 'vue'
import { linearScale, createColorMap, createOpacityMap } from '@colormap/core';

import type { ColorNode, ColorOpacityNode, OpacityNode, Vector4D } from '@/types'
import { MapNodeAdapter } from '@/utils/nodes';

const props = defineProps<{
  colorNodes: ColorNode[];
  opacityNodes: OpacityNode[];
}>();

const adaptedColorNodes = computed(() => props.colorNodes.map((el) => new MapNodeAdapter(el)));
const adaptedOpacityNodes = computed(() => props.opacityNodes.map((el) => new MapNodeAdapter(el)));

const colorOpacityNodes = computed(() => {
    const scale = linearScale([0, 1], [0, 1]);
    const colormapFn = createColorMap(adaptedColorNodes.value, scale);
    const opacitymapFn = createOpacityMap(adaptedOpacityNodes.value, scale);

    const colorOpacityNodes: ColorOpacityNode[] = [];

    let i = 0;
    let j = 0;

    while (i < adaptedColorNodes.value.length && j < adaptedOpacityNodes.value.length) {
        let colorValue: number = Infinity;
        let opacityValue: number = Infinity;
        let value: number = 0;

        if (i < adaptedColorNodes.value.length) {
            colorValue = adaptedColorNodes.value[i]!.value;
        }

        if (j < adaptedOpacityNodes.value.length) {
            opacityValue = adaptedOpacityNodes.value[j]!.value;
        }

        if (colorValue == opacityValue) {
            value = colorValue;
            i++;
            j++;
        } else if (colorValue < opacityValue) {
            value = colorValue;
            i++;
        } else {
            value = opacityValue;
            j++;
        }

        let mapped: Vector4D = [...colormapFn(value), opacitymapFn(value)];
        colorOpacityNodes.push([value, mapped]);
    }

    return colorOpacityNodes;
});

</script>

<template>
    <slot
        :colorOpacityNodes
    ></slot>
</template>

<style scoped>
</style>
