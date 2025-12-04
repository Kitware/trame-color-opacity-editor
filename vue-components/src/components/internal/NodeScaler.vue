<script setup lang="ts" generic="T">
import { defineProps, computed, withDefaults } from "vue";

import type { MapNode, Vector2D } from "@/types";

import { unscaleNode, scaleNodes, unscaleNodes } from "@/utils/nodes";

const props = withDefaults(
  defineProps<{
    xRange?: Vector2D;
    yRange?: Vector2D;
    xLog?: boolean;
    yLog?: boolean;
  }>(),
  {
    xLog: false,
    yLog: false,
  },
);

const nodes = defineModel<MapNode<T>[]>("nodes", {
  required: true,
});

const emit = defineEmits<{
  nodeModified: [[index: number, node: MapNode<T>]];
  nodeAdded: [[index: number, node: MapNode<T>]];
  nodeRemoved: [index: number];
}>();

defineSlots<{
  default(props: {
    scaledNodes: MapNode<T>[];
    scaledNodesUpdated(nodes: MapNode<T>[]): void;
    scaledNodeModified([index, node]: [number, MapNode<T>]): void;
    scaledNodeAdded([index, node]: [number, MapNode<T>]): void;
    scaledNodeRemoved(index: number): void;
  }): void;
}>();

const scaledNodes = computed(() => {
  return scaleNodes(nodes.value, props.xRange, props.yRange);
});

function onScaledNodesUpdated(newScaledNodes: MapNode<T>[]) {
  nodes.value = unscaleNodes(
    newScaledNodes,
    props.xRange,
    props.yRange,
  );
}

function onScaledNodesNodeModified([index, node]: [number, MapNode<T>]) {
  node = unscaleNode(node, props.xRange, props.yRange);

  emit("nodeModified", [index, node]);
}

function onScaledNodesNodeAdded([index, node]: [number, MapNode<T>]) {
  node = unscaleNode(node, props.xRange, props.yRange);

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

<style scoped></style>
