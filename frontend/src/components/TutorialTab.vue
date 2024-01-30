<script setup>
defineProps({
  tabTitle: {
    type: String,
    required: true
  }
})
</script>

<template>
  <div class="w-full h-auto bg-dracula-theme border-neutral-200 border-b-2 border-x-2 text-center text-lg font-normal text-neutral-100 cursor-pointer hover:bg-neutral-600">
    {{ tabTitle }}
  </div>
</template>

<style scoped>
</style>
