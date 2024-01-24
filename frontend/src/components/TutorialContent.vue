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

import { ref, shallowRef } from 'vue'

const MONACO_EDITOR_OPTIONS = {
  automaticLayout: true,
  formatOnType: true,
  formatOnPaste: true,
}

const code = ref('# some code...')
const editorRef = shallowRef()
const handleMount = editor => (editorRef.value = editor)
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

      <div class="h-[50vh]">
        <vue-monaco-editor
          v-model:value="code"
          theme="vs-dark"
          languge="python"
          :options="MONACO_EDITOR_OPTIONS"
          @mount="handleMount"
        />
      </div>

      <p class="font-light text-xs">
          Please execute this code on your machine. Our code execution engine is curently a work in progress!
      </p>
  </div>
</template>
