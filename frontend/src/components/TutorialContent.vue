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

import { ref } from 'vue'

// *** Code Mirror Dependencies *** //
import Codemirror from "codemirror-editor-vue3";
// language
import "codemirror/mode/python/python.js";
// placeholder
import "codemirror/addon/display/placeholder.js";
// autorefresh
import "codemirror/addon/display/autorefresh.js";
// theme
import "codemirror/theme/dracula.css";
// ******************************* //

const currentOutlineStep = ref(0)
const showModal = ref(false)
const code = ref(
`def main():
  print("Hello World!")
}`
);
const exampleCode = ref(props.content["code"])

const cmOptions = {
        mode: "text/x-python", // Language mode
        theme: "dracula", // Theme
      }

const cmExampleOptions = {
  mode: "text/x-python", // Language mode
  theme: "dracula", // Theme
  readOnly: true, // Read Only
  autoRefresh: true, // Allow for autorefresh
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

      <div class="grid grid-cols-10 w-full font-medium text-l mt-3">
          <span class="col-span-8">
            <span>Step {{ currentOutlineStep + 1 }}:</span>
            <span>{{ content["outline"][currentOutlineStep] }}</span>
          </span>

          <span class="col-span-2 text-center">
            <span class="ml-2 cursor-pointer" @click="decrementStep">
              <IconSvg name="angles-left" size="15px" class="inline"/>Prev
            </span>
            |
            <span class="cursor-pointer" @click="incrementStep">
              Next<IconSvg name="angles-right" size="15px" class="inline"/>
            </span>
          </span>
      </div>

      <div class="h-[60vh] mt-3">
        <Codemirror
          v-model:value="code"
          :options="cmOptions"
        />
      </div>

      <div class="grid grid-cols-10 w-full mt-3">
        <p class="font-light text-xs col-span-8">
            Please execute this code on your machine. Our code execution engine is curently a work in progress!
        </p>
        <div class="col-span-2 text-right">
          <span class="inline-block mr-2">
            <button class="bg-green-400 rounded-lg font-bold text-l border-black border p-2.5" @click="console.log('This button does nothing!')">Run Code</button>
          </span>
          <span class="float-right" title="Send Help!" @click="showModal = true">
            <IconSvg class="bg-gray-400 rounded-full p-2" name="lightbulb" size="40px" color="yellow"/>
          </span>
        </div>
      </div>

      <vue-final-modal
        v-bind="$attrs"
        v-model="showModal"
        classes="flex justify-center items-center"
        content-class="relative flex flex-col max-h-full w-3/5 mx-4 p-4 border dark:border-gray-800 rounded bg-white dark:bg-gray-900"
      >
        <span class="mr-8 text-2xl font-bold">
          <h4>Code Hints and Explanation</h4>
        </span>
        <hr/>
        <div class="flex-grow overflow-y-auto">
          <span>
            <Codemirror
              v-model:value="exampleCode"
              :options="cmExampleOptions"
            />
            {{  }}
          </span>
          <hr/>
          <span>{{ content["explanation"] }}</span>
        </div>
        <button class="absolute top-0 right-0 mt-2 mr-2 p-2 rounded-lg hover:border-gray-300 hover:bg-gray-100 hover:dark:border-neutral-700 hover:dark:bg-neutral-800/30" @click="showModal = false">
          <IconSvg name="x" size="15px" />
        </button>
      </vue-final-modal>

  </div>
</template>
