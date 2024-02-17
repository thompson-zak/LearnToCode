<script setup>
const props = defineProps({
  section: {
    type: String,
    required: true
  },
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
import { VueSpinnerGears } from 'vue3-spinners';

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

const code = ref("");
const codePlaceholder = 
`message = "Hello World!"
print(message)`;

const exampleCode = ref(props.content["code"])
const outputResult = ref("")
const isCodeExecuting = ref(false)

const cmOptions = {
        mode: "text/x-python", // Language mode
        theme: "dracula", // Theme
      }

const cmReadOnlyOptions = {
  mode: "text/x-python", // Language mode
  theme: "dracula", // Theme
  readOnly: true, // Read Only
  autoRefresh: true, // Allow for autorefresh
}

loadCode();

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

function executeCode() {
  // First, remove previous output so there's no confusion
  outputResult.value = "";
  isCodeExecuting.value = true;

  // First parameter is endpoint URL, second is header object
  // TODO - error handling
  let endpoint = import.meta.env.VITE_API_URL;
  let requestOptions = { 
    method: "POST",
    body: JSON.stringify({ "code" : String(code.value) })
  }
  console.log(requestOptions)
  fetch(endpoint + "/execute/code", requestOptions)
      .then(async response => {
          const data = await response.json()

          console.log(data)

          if(response.ok) {
            const output = data["output"];
            outputResult.value = output;
            isCodeExecuting.value = false;
          } else {
            const errorType = data["detail"]["errorType"];
            const errorMessage = data["detail"]["errorMessage"];
            const errorFormatted = errorType + "\n\n" + errorMessage;
            outputResult.value = errorFormatted;
            isCodeExecuting.value = false;
          }
      })
}

function saveCode() {
  const key = props.section + "Code" + props.title.slice(-1);
  localStorage.setItem(key, code.value)
}

function loadCode() {
  const key = props.section + "Code" + props.title.slice(-1);
  const savedCode = localStorage.getItem(key)
  console.log(savedCode);
  if(savedCode != null) {
    code.value = savedCode;
  } else {
    code.value = codePlaceholder;
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

      <div class="grid grid-cols-10 w-full font-medium text-l my-3">
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

      <hr/>

      <h2 class="mt-3">Code:</h2>
      <div class="relative h-[45vh]">
        <Codemirror
          v-model:value="code"
          :options="cmOptions"
        />
        <div class="absolute top-0 right-0 z-10" title="Send Help!" @click="showModal = true">
          <!-- Add reference sheet modal button here -->
          <IconSvg class="bg-gray-600 rounded-full p-1.5 mt-1 mr-1" name="lightbulb" size="30px" color="yellow"/>
        </div>
        <div class="absolute bottom-0 right-0 z-10">
          <button class="bg-blue-400 rounded-lg font-bold text-l border-black border px-2.5 py-1 mb-1 mr-1" @click="saveCode">Save</button>
          <button class="bg-green-400 rounded-lg font-bold text-l border-black border px-2.5 py-1 mb-1 mr-1" @click="executeCode">Execute</button>
        </div>
      </div>

      <h2 class="mt-3">Output:</h2>
      <div class="relative h-[15vh]">
        <Codemirror
          v-model:value="outputResult"
          :options="cmReadOnlyOptions"
        />
        <VueSpinnerGears 
          v-if="isCodeExecuting === true"
          size="25" 
          color="orange"
          class="absolute bottom-2 right-2 z-10" 
        />
      </div>

      <!-- Add reference sheet modal here -->

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
              :options="cmReadOnlyOptions"
            />
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
