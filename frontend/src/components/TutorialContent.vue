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
import Constants from '../constants/config.js'

const MONACO_EDITOR_OPTIONS = {
  automaticLayout: true,
  formatOnType: true,
  formatOnPaste: true,
  autoIndent: true,
}

const code = ref(Constants.CODE_SKELETON)
const editorRef = shallowRef()
const handleMount = editor => (editorRef.value = editor)

function formatCode() {
  console.log('this is happening on keyup')
  editorRef.value?.getAction('editor.action.formatDocument').run()
}
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

      <div class="h-[60vh]">
        <vue-monaco-editor
          v-model:value="code"
          theme="vs-dark"
          languge="python"
          :options="MONACO_EDITOR_OPTIONS"
          @mount="handleMount"
          @keyup="formatCode"
        />
      </div>

      <p class="font-light text-xs">
          Please execute this code on your machine. Our code execution engine is curently a work in progress!
      </p>
  </div>
</template>
