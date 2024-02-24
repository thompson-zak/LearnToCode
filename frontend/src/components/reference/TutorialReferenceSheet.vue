<script setup>
const props = defineProps({
    section: {
        type: String,
        required: true
    },
    title: {
        type: String,
        required: true
    }
})

import VariablesContent from './VariablesContent.vue';
import DataContent from './DataContent.vue';
import ConditionalsContent from './ConditionalsContent.vue';
import LoopsContent from './LoopsContent.vue';
</script>

<template>
    <span class="mr-8 mb-2 text-2xl font-bold">
        <h4>{{ title }}</h4>
    </span>
    <hr/>
    <div class="mt-2">
        <VariablesContent v-if="props.section == 'Variables'" />

        <DataContent v-if="props.section == 'Data'" />

        <ConditionalsContent v-if="props.section == 'Conditionals'" />

        <LoopsContent v-if="props.section == 'Loops'" />
    </div>
</template>

<style>
</style>