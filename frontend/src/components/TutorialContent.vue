<script setup>
const props = defineProps({
  title: {
    type: String,
    required: true
  },
  description: {
    type: String,
    required: true
  },
  content: {
    type: Object,
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

const currentOutlineStep = ref(0)

function formatCode() {
  console.log('this is happening on keyup')
  editorRef.value?.getAction('editor.action.formatDocument').run()
}

function decrementStep() {
  if (currentOutlineStep.value > 0) {
    currentOutlineStep.value = currentOutlineStep.value - 1;
  }
}

function incrementStep() {
  if (currentOutlineStep.value < props.content["outline"].length - 1) {
    currentOutlineStep.value = currentOutlineStep.value + 1;
  }
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
          {{ content["prompt"] }}
      </div>

      <div class="font-medium text-l mt-3">
          <span>Step {{ currentOutlineStep + 1 }}:</span>
          <span>{{ content["outline"][currentOutlineStep] }}</span>

          <span class="ml-2" @click="decrementStep">
            <IconSvg name="angles-left" size="15px" class="inline"/>Prev
          </span>
          |
          <span @click="incrementStep">
            Next<IconSvg name="angles-right" size="15px" class="inline"/>
          </span>
      </div>

      <div class="h-[60vh] mt-3">
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
