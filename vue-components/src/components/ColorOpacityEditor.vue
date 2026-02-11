<script setup lang="ts">
import { defineModel, withDefaults } from 'vue'

import { type ColorNode, type OpacityNode, type RGBAColor, type Vector2D } from '@/types'
import NodeScaler from '@/components/internal/NodeScaler.vue'
import ViewportContainer from '@/components/internal/ViewportContainer.vue'
import BackgroundShaper from './internal/BackgroundShaper.vue'
import BackgroundView from './internal/BackgroundView.vue'
import ControlsView from './internal/ControlsView.vue'
import NodeMerger from './internal/NodeMerger.vue'
import BackgroundShaperFull from './internal/BackgroundShaperFull.vue'
import NodeFlattener from './internal/NodeFlattener.vue'
import BackgroundShaperHistograms from './internal/BackgroundShaperHistograms.vue'
import { isColorNode, isOpacityNode } from '@/utils/nodes'

interface Props {
  scalarRange: Vector2D
  histogramsRange: Vector2D
  backgroundShape: 'full' | 'opacity' | 'histograms'
  backgroundOpacity: boolean
  histograms: Vector2D[]
  showHistograms: boolean
  showOpacityEditor: boolean
  showColorEditor: boolean
  style: string
  viewportPadding: Vector2D
  histogramsColor: RGBAColor
  handleColor: RGBAColor
  handleBorderColor: RGBAColor
  handleRadius: number
  lineWidth: number
}

type Events = {
  colorNodeModified: [[index: number, node: ColorNode]]
  colorNodeAdded: [[index: number, node: ColorNode]]
  colorNodeRemoved: [index: number]
  opacityNodeModified: [[index: number, node: OpacityNode]]
  opacityNodeAdded: [[index: number, node: OpacityNode]]
  opacityNodeRemoved: [index: number]
}

withDefaults(defineProps<Props>(), {
  backgroundShape: 'opacity',
  showHistograms: false,
  showOpacityEditor: true,
  showColorEditor: true,
  histogramsColor: () => [0, 0, 0, 0.25],
  viewportPadding: () => [8, 8],
  handleColor: () => [0.125, 0.125, 0.125, 1],
  handleBorderColor: () => [0.75, 0.75, 0.75, 1],
  handleRadius: 7,
  lineWidth: 2,
})

const emit = defineEmits<Events>()

const colorNodes = defineModel<ColorNode[]>('colorNodes', {
  required: true,
})

const opacityNodes = defineModel<OpacityNode[]>('opacityNodes', {
  required: true,
})

function onOpacityNodeModified([index, node]: [number, ColorNode | OpacityNode]) {
  if (isOpacityNode(node)) {
    emit('opacityNodeModified', [index, node])
  }
}

function onOpacityNodeAdded([index, node]: [number, ColorNode | OpacityNode]) {
  if (isOpacityNode(node)) {
    emit('opacityNodeAdded', [index, node])
  }
}

function onOpacityNodeRemoved(index: number) {
  console.log('onOpacityNodeRemoved', index)
  emit('opacityNodeRemoved', index)
}

function onColorNodeModified([index, node]: [number, ColorNode | OpacityNode]) {
  if (isColorNode(node)) {
    emit('colorNodeModified', [index, node])
  }
}

function onColorNodeAdded([index, node]: [number, ColorNode | OpacityNode]) {
  if (isColorNode(node)) {
    emit('colorNodeAdded', [index, node])
  }
}

function onColorNodeRemoved(index: number) {
  emit('colorNodeRemoved', index)
}
</script>

<template>
  <div class="color-opacity-editor-root-container" :style="style">
    <NodeScaler
      :nodes="histograms"
      :xRange="scalarRange"
      :yRange="histogramsRange"
      v-slot="{ scaledNodes: scaledHistograms }"
    >
      <NodeScaler
        v-model:nodes="colorNodes"
        :xRange="scalarRange"
        @nodeModified="onColorNodeModified"
        @nodeAdded="onColorNodeAdded"
        @nodeRemoved="onColorNodeRemoved"
        v-slot="{
          scaledNodes: scaledColorNodes,
          scaledNodesUpdated: scaledColorNodesUpdated,
          scaledNodeModified: scaledColorNodeModified,
          scaledNodeAdded: scaledColorNodeAdded,
          scaledNodeRemoved: scaledColorNodeRemoved,
        }"
      >
        <NodeScaler
          v-model:nodes="opacityNodes"
          :xRange="scalarRange"
          @nodeModified="onOpacityNodeModified"
          @nodeAdded="onOpacityNodeAdded"
          @nodeRemoved="onOpacityNodeRemoved"
          v-slot="{
            scaledNodes: scaledOpacityNodes,
            scaledNodesUpdated: scaledOpacityNodesUpdated,
            scaledNodeModified: scaledOpacityNodeModified,
            scaledNodeAdded: scaledOpacityNodeAdded,
            scaledNodeRemoved: scaledOpacityNodeRemoved,
          }"
        >
          <ViewportContainer
            v-if="showOpacityEditor"
            v-slot="{ viewportSize }"
            class="color-opacity-editor-opacity-container"
          >
            <BackgroundShaper
              :backgroundShape
              :opacityNodes="scaledOpacityNodes"
              :histograms="scaledHistograms"
              v-slot="{ shape }"
            >
              <NodeMerger
                v-if="backgroundOpacity"
                :colorNodes="scaledColorNodes"
                :opacityNodes="scaledOpacityNodes"
                v-slot="{ colorOpacityNodes }"
              >
                <BackgroundView
                  :shape
                  :size="viewportSize"
                  :padding="viewportPadding"
                  :nodes="colorOpacityNodes"
                ></BackgroundView>
              </NodeMerger>
              <BackgroundView
                v-else
                :shape
                :size="viewportSize"
                :padding="viewportPadding"
                :nodes="scaledColorNodes"
              ></BackgroundView>
            </BackgroundShaper>

            <BackgroundShaperHistograms
              v-if="showHistograms"
              :nodes="scaledHistograms"
              v-slot="{ shape }"
            >
              <BackgroundView
                :shape
                :size="viewportSize"
                :padding="viewportPadding"
                :nodes="[[0, histogramsColor]]"
                class="color-opacity-editor-canvas"
              ></BackgroundView>
            </BackgroundShaperHistograms>

            <ControlsView
              :size="viewportSize"
              :padding="viewportPadding"
              showLine
              :radius="handleRadius"
              :lineWidth="lineWidth"
              :color="handleColor"
              :borderColor="handleBorderColor"
              :nodes="scaledOpacityNodes"
              @update:nodes="scaledOpacityNodesUpdated"
              @nodeModified="scaledOpacityNodeModified"
              @nodeAdded="scaledOpacityNodeAdded"
              @nodeRemoved="scaledOpacityNodeRemoved"
            ></ControlsView>
          </ViewportContainer>

          <ViewportContainer
            v-if="showColorEditor"
            v-slot="{ viewportSize }"
            class="color-opacity-editor-color-container"
          >
            <BackgroundShaperFull v-slot="{ shape }">
              <BackgroundView
                :shape
                :size="viewportSize"
                :padding="viewportPadding"
                :nodes="scaledColorNodes"
              ></BackgroundView>
            </BackgroundShaperFull>
            <NodeFlattener
              :nodes="scaledColorNodes"
              @update:nodes="scaledColorNodesUpdated"
              @nodeModified="scaledColorNodeModified"
              @nodeAdded="scaledColorNodeAdded"
              @nodeRemoved="scaledColorNodeRemoved"
              :slotPropsNames="{ flattenedNodes: 'flattenedColorNodes' }"
              v-slot="{
                flattenedNodes: flattenedColorNodes,
                flattenedNodesUpdated: flattenedColorNodesUpdated,
                flattenedNodeModified: flattenedColorNodeModified,
                flattenedNodeAdded: flattenedColorNodeAdded,
                flattenedNodeRemoved: flattenedColorNodeRemoved,
              }"
            >
              <ControlsView
                :size="viewportSize"
                :padding="[viewportPadding[0], 0]"
                :lineWidth="0"
                :radius="handleRadius"
                :color="handleColor"
                :borderColor="handleBorderColor"
                :showLine="false"
                :nodes="flattenedColorNodes"
                @update:nodes="flattenedColorNodesUpdated"
                @nodeModified="flattenedColorNodeModified"
                @nodeAdded="flattenedColorNodeAdded"
                @nodeRemoved="flattenedColorNodeRemoved"
              ></ControlsView>
            </NodeFlattener>
          </ViewportContainer>
        </NodeScaler>
      </NodeScaler>
    </NodeScaler>
  </div>
</template>

<style scoped>
.color-opacity-editor-root-container {
  display: flex;
  flex-direction: column;
}

.color-opacity-editor-opacity-container {
  width: 100%;
  flex-grow: 1;
  position: relative;
  overflow: hidden;
}

.color-opacity-editor-canvas {
  position: absolute;
  top: 0;
  left: 0;
}

.color-opacity-editor-color-container {
  width: 100%;
  height: 2.5rem;
  position: relative;
  overflow: hidden;
}
</style>
