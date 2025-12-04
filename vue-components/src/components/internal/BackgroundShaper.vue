<script setup lang="ts">
import { defineProps } from 'vue'
import BackgroundShaperFull from './BackgroundShaperFull.vue';
import BackgroundShaperOpacity from './BackgroundShaperOpacity.vue';
import BackgroundShaperHistograms from './BackgroundShaperHistograms.vue';
import type { OpacityNode, Vector2D } from '@/types';



const props = defineProps<{
    backgroundShape: "full" | "opacity" | "histograms";
    opacityNodes?:OpacityNode[];
    histograms?: Vector2D[];
}>();

defineSlots<{
    default(props: {
        shape: Vector2D[];
    }): void;
}>();

</script>

<template>
    <BackgroundShaperOpacity v-if="opacityNodes && backgroundShape==='opacity'" :nodes="opacityNodes" v-slot="{ shape }">
        <slot :shape ></slot>
    </BackgroundShaperOpacity>

    <BackgroundShaperHistograms v-else-if="histograms && backgroundShape==='histograms'" :nodes="histograms" v-slot="{ shape }">
        <slot :shape ></slot>
    </BackgroundShaperHistograms>

    <BackgroundShaperFull v-else v-slot="{ shape }">
        <slot :shape ></slot>
    </BackgroundShaperFull>
</template>

<style scoped>
</style>
