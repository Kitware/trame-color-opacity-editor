<script setup lang="ts">
import { defineProps, useTemplateRef, defineModel, onMounted, computed, watch, withDefaults, ref } from 'vue'
import type { OpacityNode, RGBAColor } from '@/types'
import type { Vector2D } from '@/types'
import { clampNodeToBounds, drawCanvasControls, getNodeBounds, mouseToPixel, pickNodeOnCanvas, pixelToFraction } from '@/utils/canvas';

interface Props {
    color: RGBAColor;
    borderColor: RGBAColor;
    size: Vector2D;
    padding: Vector2D;
    radius: number;
    showLine: boolean;
    lineWidth: number;
}

const props = withDefaults(defineProps<Props>(), {
    radius: 7,
    padding: () => [7, 7],
    color: () => [0.125, 0.125, 0.125, 1],
    borderColor: () => [0.75, 0.75, 0.75, 1],
    showLine: true,
    lineWidth: 3,
});

const nodes = defineModel<OpacityNode[]>("nodes", {
  required: true,
});

const emit = defineEmits<{
    nodeModified: [[index: number, node: OpacityNode]];
    nodeAdded: [[index: number, node: OpacityNode]];
    nodeRemoved: [index: number];
}>();

const canvas = useTemplateRef<HTMLCanvasElement>("controls-canvas");
const pickingCanvas = useTemplateRef<HTMLCanvasElement>("pick-canvas");

const activeNodeId = ref<number>(-1);

const contentSize = computed<Vector2D>(() => [
    Math.max(props.size[0] - 2 * props.padding[0], 0),
    Math.max(props.size[1] - 2 * props.padding[1], 0)
]);

const fillColor = computed<RGBAColor>(() => [props.color[0] * 255, props.color[1] * 255, props.color[2] * 255, props.color[3]]);
const outerColor = computed<RGBAColor>(() => [props.borderColor[0] * 255, props.borderColor[1] * 255, props.borderColor[2] * 255, props.borderColor[3]]);

watch(() => [canvas, pickingCanvas, props.size, props.padding, nodes.value, props.radius, props.showLine, props.lineWidth, fillColor, outerColor], () => {
    if (!canvas.value || !pickingCanvas.value) {
        return;
    }

    const context = canvas.value.getContext('2d');
    const pickingContext = pickingCanvas.value.getContext('2d');

    if (!context || !pickingContext) {
        return;
    }

    canvas.value.width = props.size[0];
    canvas.value.height = props.size[1];
    pickingCanvas.value.width = props.size[0];
    pickingCanvas.value.height = props.size[1];

    drawCanvasControls(context, pickingContext, props.size, props.padding, contentSize.value, nodes.value, props.radius, props.showLine, props.lineWidth, fillColor.value, outerColor.value);
});

onMounted(() => {
    if (!canvas.value || !pickingCanvas.value) {
        return;
    }

    const context = canvas.value.getContext('2d');
    const pickingContext = pickingCanvas.value.getContext('2d');

    if (!context || !pickingContext) {
        return;
    }

    canvas.value.width = props.size[0];
    canvas.value.height = props.size[1];
    pickingCanvas.value.width = props.size[0];
    pickingCanvas.value.height = props.size[1];

    drawCanvasControls(context, pickingContext, props.size, props.padding, contentSize.value, nodes.value, props.radius, props.showLine, props.lineWidth, fillColor.value, outerColor.value);
});

function onMouseMove(ev: MouseEvent) {
    if (activeNodeId.value < 0) {
        return;
    }

    if (!canvas.value) {
        return;
    }

    const p0 = mouseToPixel([ev.clientX, ev.clientY], canvas.value.getBoundingClientRect());
    let f0 = pixelToFraction(p0, props.size, props.padding, contentSize.value);

    const bounds = getNodeBounds(activeNodeId.value, nodes.value, 0.001);
    f0 = clampNodeToBounds(f0, bounds);

    const currentF0 = nodes.value[activeNodeId.value];

    if (currentF0 === undefined || (f0[0] == currentF0[0] && f0[1] == currentF0[1])) {
        return;
    }

    const newNodes = [...nodes.value];
    newNodes[activeNodeId.value] = f0;

    emit('nodeModified', [activeNodeId.value, f0]);
    nodes.value = newNodes;
}

function onLeftMouseDown(p: Vector2D, picked: { id: number; type: "handle" | "edge"; } | null) {
    if (picked) {
        if (picked.type === 'handle') {
            activeNodeId.value = picked.id;
        } else {
            let f0 = pixelToFraction(p, props.size, props.padding, contentSize.value);

            activeNodeId.value = picked.id + 1;

            emit('nodeAdded', [picked.id + 1, f0]);
            nodes.value = [...nodes.value.slice(0, picked.id + 1), f0, ...nodes.value.slice(picked.id + 1, nodes.value.length)];
        }

        window.addEventListener("mousemove", onMouseMove);
        window.addEventListener("mouseup", () => {
            activeNodeId.value = -1;
            window.removeEventListener("mousemove", onMouseMove);
        });
    } else {
        activeNodeId.value = -1;
    }
}

function onRightMouseDown(p: Vector2D, picked: { id: number; type: "handle" | "edge"; } | null) {
    if (nodes.value.length < 3) {
        return;
    }

    if (picked && picked.type === 'handle') {
        emit('nodeRemoved', picked.id);
        nodes.value = [...nodes.value.slice(0, picked.id), ...nodes.value.slice(picked.id + 1, nodes.value.length)];
    }
}

function onDoubleClick(ev: MouseEvent) {
    if (!canvas.value) {
        return;
    }

    if (!pickingCanvas.value) {
        return;
    }

    const ctx = pickingCanvas.value.getContext('2d');

    if (!ctx) {
        return;
    }

    const p0 = mouseToPixel([ev.clientX, ev.clientY], canvas.value.getBoundingClientRect());
    const picked = pickNodeOnCanvas(p0, ctx);

    // only create a node if we double clicked on empty space
    if (picked) {
        return;
    }

    let f0 = pixelToFraction(p0, props.size, props.padding, contentSize.value);

    let newNodeId = -1;

    for (let i = 0; i < nodes.value.length; i++) {
        if (nodes.value[i]![0] > f0[0]) {
            break;
        }

        newNodeId = i;
    }

    emit('nodeAdded', [newNodeId + 1, f0]);
    nodes.value = [...nodes.value.slice(0, newNodeId + 1), f0, ...nodes.value.slice(newNodeId + 1, nodes.value.length)];
}

function onMouseDown(ev: MouseEvent) {
    if (!canvas.value) {
        return;
    }

    if (!pickingCanvas.value) {
        return;
    }

    const ctx = pickingCanvas.value.getContext('2d');

    if (!ctx) {
        return;
    }

    const p0 = mouseToPixel([ev.clientX, ev.clientY], canvas.value.getBoundingClientRect());
    const picked = pickNodeOnCanvas(p0, ctx);

    if (ev.button == 0) {
        onLeftMouseDown(p0, picked);
    } else if (ev.button == 1) {
        // Middle button
    } else {
        // Right button
        onRightMouseDown(p0, picked);
    }
}
</script>

<template>
    <div class="fill">
        <canvas class="fill controls-canvas picking-canvas" ref="pick-canvas"></canvas>
        <canvas
            @dblclick="onDoubleClick"
            @mousedown="onMouseDown"
            @contextmenu="(ev) => ev.preventDefault()"
            class="fill controls-canvas" ref="controls-canvas"
        ></canvas>
    </div>
</template>

<style scoped>
.fill {
  width: 100%;
  height: 100%;
}

.controls-canvas {
    position: absolute;
    top: 0;
    left: 0;
}

.picking-canvas {
    visibility: hidden;
}
</style>
