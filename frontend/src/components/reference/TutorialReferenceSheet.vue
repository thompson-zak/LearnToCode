<script setup>
const props = defineProps({
    section: {
        type: String,
        required: true
    }
})

import VariablesContent from './VariablesContent.vue';
</script>

<template>
    <span class="mr-8 mb-2 text-2xl font-bold">
        <h4>Reference Sheet</h4>
    </span>
    <hr/>
    <div class="mt-2">
        <VariablesContent v-if="props.section == 'Variables'" />
    </div>
</template>

<style>
</style>