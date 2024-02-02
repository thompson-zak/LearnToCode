<script setup>
import { ref } from 'vue';

const displayIndex = ref(1)

// Every 5 seconds, switch to the next piece of text
setInterval(() => {
    if(displayIndex.value == 4) {
        displayIndex.value = 1;
    } else {
        displayIndex.value = displayIndex.value + 1;
    }
}, 5000)

</script>

<template>
    <div>
        <p v-if="displayIndex == 1">Using the power of AI to generate a custom lesson plan just for you</p>
        <p v-if="displayIndex == 2">Talking with ChatGPT to get all new coding problems</p>
        <p v-if="displayIndex == 3">Only a moment longer...</p>
        <p v-if="displayIndex == 4">Seriously, what is taking so long?!?!?!</p>
    </div>
</template>

<style></style>