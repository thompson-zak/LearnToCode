<script setup>
defineProps({
  title: {
    type: String,
    required: true
  },
  description: {
    type: String,
    required: true
  },
  gptPrompt: {
    type: String,
    required: true
  }
})
</script>

<template>
  <div class="w-full">
      <div class="font-bold text-2xl">
          {{ title }}
      </div>
      <div class="font-medium text-xs w-auto inline-block border-b border-black">
          {{ description }}
      </div>

      <div class="font-medium text-l mt-3">
          {{ gptPrompt }}
      </div>
      <p>
        TODO: The editor will go here.
      </p>
      <p class="font-light text-xs">
          Please execute this code on your machine. Our code execution engine is curently a work in progress!
      </p>
  </div>
</template>
