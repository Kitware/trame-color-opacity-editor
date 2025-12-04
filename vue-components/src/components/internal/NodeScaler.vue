<script setup lang="ts" generic="T extends OpacityNode | ColorNode">
import { defineProps, computed, withDefaults } from 'vue'

import type { ColorNode, ColorOpacityNode, OpacityNode, Vector2D } from '@/types'

import {
    isColorNodes,
    unscaleNode,
    scaleNodeX, scaleNodeY,
    scaleNodesX, scaleNodesY,
    unscaleNodeX, unscaleNodeY,
    unscaleNodesX, unscaleNodesY,
    scaleNodes, unscaleNodes,
} from '@/utils/nodes';


type SlotPropsNames = {
  scaledNodes: string;
};

const props = withDefaults(defineProps<{
    xRange?: Vector2D;
    yRange?: Vector2D;
    xLog?: boolean;
    yLog?: boolean;
    slotPropsNames?: SlotPropsNames;
}>(), {
    slotPropsNames: () => ({scaledNodes: "scaledNodes"}),
    xLog: false,
    yLog: false,
});

const nodes = defineModel<T[]>("nodes", {
  required: true,
});

const emit = defineEmits<{
    nodeModified: [[index: number, node: T]];
    nodeAdded: [[index: number, node: T]];
    nodeRemoved: [index: number];
}>();

defineSlots<{
    default(props: {
        scaledNodes: T[];
        scaledNodesUpdated(nodes: T[]): void;
        scaledNodeModified([index, node]: [number, T]): void;
        scaledNodeAdded([index, node]: [number, T]): void;
        scaledNodeRemoved(index: number): void;
    }): void;
}>();

const scaledNodes = computed(() => {
    return scaleNodes(nodes.value as any, props.xRange, props.yRange) as T[];
});

function onScaledNodesUpdated(newScaledNodes: T[]) {
    nodes.value = unscaleNodes(newScaledNodes as any, props.xRange, props.yRange) as T[];
}

function onScaledNodesNodeModified([index, node]: [number, T]) {
    node = unscaleNode(node as any, props.xRange, props.yRange) as T;

    emit("nodeModified", [index, node]);
}

function onScaledNodesNodeAdded([index, node]: [number, T]) {
    node = unscaleNode(node as any, props.xRange, props.yRange) as T;

    emit("nodeAdded", [index, node]);
}

function onScaledNodesNodeRemoved(index: number) {
    emit("nodeRemoved", index);
}

</script>

<template>
    <slot
        :scaledNodes
        :scaledNodesUpdated="onScaledNodesUpdated"
        :scaledNodeModified="onScaledNodesNodeModified"
        :scaledNodeAdded="onScaledNodesNodeAdded"
        :scaledNodeRemoved="onScaledNodesNodeRemoved"
    ></slot>
</template>

<style scoped>
</style>
