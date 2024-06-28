<script setup>
const exercises = [
    {
        section: "Variables",
        id: 1,
    },
    {
        section: "Variables",
        id: 2,
    },
    {
        section: "Data",
        id: 1,
    },
    {
        section: "Data",
        id: 2,
    },
    {
        section: "Conditionals",
        id: 1,
    },
    {
        section: "Conditionals",
        id: 2,
    },
    {
        section: "Loops",
        id: 1,
    },
    {
        section: "Loops",
        id: 2,
    },
]

import { usePointsStore } from '@/stores/PointsStore';

const pointsStore = usePointsStore();
</script>

<template>
  <div class="w-full h-auto p-2 border-4 rounded-lg border-zinc-500">
    <h1 class="font-bold text-2xl mb-2 border-b-2 border-zinc-500">
        Your Progress
    </h1>

    <div v-for="(exercise, index) in exercises" :key="index" class="mb-2">
        <IconSvg v-if="pointsStore.getPoints(exercise.section, exercise.id) >= 1" name="check" size="20px" color="green" class="inline-block mr-2"></IconSvg>
        <IconSvg v-else name="ellipsis" size="20px" color="rgb(255, 191, 0)" class="inline-block mr-2"></IconSvg>
        {{ exercise.section }} - {{ exercise.id }}
    </div>
  </div>
</template>

<style scoped>
</style>