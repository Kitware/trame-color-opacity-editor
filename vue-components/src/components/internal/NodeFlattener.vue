<script setup lang="ts">
import { defineProps, defineSlots, computed } from 'vue'
import { linearScale, createColorMap } from '@colormap/core';

import type { ColorNode, OpacityNode } from '@/types'
import { MapNodeAdapter } from '@/utils/nodes';

type SlotPropsNames = {
  flattenedNodes: string;
};


const props = defineProps<{
    nodes: ColorNode[];
    slotPropsNames: SlotPropsNames;
}>();

const nodes = defineModel<ColorNode[]>("nodes", {
  required: true,
});

const emit = defineEmits<{
    nodeModified: [[index: number, node: ColorNode]];
    nodeAdded: [[index: number, node: ColorNode]];
    nodeRemoved: [index: number];
}>();

defineSlots<{
    default(props: {
        flattenedNodes: OpacityNode[];
        flattenedNodesUpdated(nodes: OpacityNode[]): void;
        flattenedNodeModified([index, node]: [number, OpacityNode]): void;
        flattenedNodeAdded([index, node]: [number, OpacityNode]): void;
        flattenedNodeRemoved(index: number): void;
    }): void;
}>();

const flattenedNodes = computed(() => props.nodes.map((el) => [el[0], 0.5] as OpacityNode));

function flattenedNodesUpdated(newFlattenedNodes: OpacityNode[]) {
    // console.log("NODES UPDATEDDD", newFlattenedNodes);
    const currentNodes = [...props.nodes];

    if (currentNodes.length == newFlattenedNodes.length) {
        const newNodes = newFlattenedNodes.map((el, i) => {
            return [el[0], currentNodes[i]![1]] as ColorNode;
        });

        nodes.value = newNodes;
    } else {
        const adaptedColorNodes = currentNodes.map((el) => new MapNodeAdapter(el));
        const scale = linearScale([0, 1], [0, 1]);
        const colormapFn = createColorMap(adaptedColorNodes, scale);

        const epsilon = 0.0001;

        let currNodeId = 0;

        const newNodes: ColorNode[] = [];

        for (let i = 0; i < newFlattenedNodes.length; i ++) {
            if (Math.abs(currentNodes[currNodeId]![0] - newFlattenedNodes[i]![0]) < epsilon) {
                newNodes.push([newFlattenedNodes[i]![0], currentNodes[currNodeId]![1]]);
                currNodeId++;
            } else {
                newNodes.push([newFlattenedNodes[i]![0], colormapFn(newFlattenedNodes[i]![0])]);
            }
        }

        nodes.value = newNodes;
    }
}

function onflattenedNodesNodeModified([index, node]: [number, OpacityNode]) {
    if (index >= props.nodes.length) {
        return;
    }

    const newNode: ColorNode = [node[0], props.nodes[index]![1]]

    emit("nodeModified", [index, newNode]);
}

function onflattenedNodesNodeAdded([index, node]: [number, OpacityNode]) {
    const n = props.nodes.length;

    if (n < 1) {
        return;
    }

    if (index <= 0) {
        const newNode: ColorNode = [node[0], props.nodes[0]![1]];
        emit("nodeAdded", [0, newNode]);
    } else if (index >= n) {
        const newNode: ColorNode = [node[0], props.nodes[n]![1]];
        emit("nodeAdded", [n, newNode]);
    } else {
        const adaptedColorNodes = props.nodes.map((el) => new MapNodeAdapter(el));
        const scale = linearScale([0, 1], [0, 1]);
        const colormapFn = createColorMap(adaptedColorNodes, scale);
        const newNode: ColorNode = [node[0], colormapFn(node[0])];
        emit("nodeAdded", [index, newNode]);
    }
}

function onflattenedNodesNodeRemoved(index: number) {
    emit("nodeRemoved", index);
}

</script>

<template>
    <slot
        :flattenedNodes
        :flattenedNodesUpdated="flattenedNodesUpdated"
        :flattenedNodeModified="onflattenedNodesNodeModified"
        :flattenedNodeAdded="onflattenedNodesNodeAdded"
        :flattenedNodeRemoved="onflattenedNodesNodeRemoved"
    ></slot>
</template>

<style scoped>
</style>
