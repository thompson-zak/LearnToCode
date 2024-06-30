<script setup>
const props = defineProps({
  section: {
    type: String,
    required: true
  },
  id: {
    type: Number,
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
import TutorialReferenceSheet from './reference/TutorialReferenceSheet.vue';
import Modal from '../components/CodeResultModal.vue';
import { useLoginStore } from '@/stores/LoginStore';
import { usePointsStore } from '@/stores/PointsStore';

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

const loginStore = useLoginStore();
const pointsStore = usePointsStore();

const currentOutlineStep = ref(0);
const showHintModal = ref(false);
const showReferenceModal = ref(false);
const showResultModal = ref(false);
const showSuccessInResultModal = ref(false);

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

const cmReadOnlyOptionsOutput = {
  mode: null, // Language mode
  theme: "dracula", // Theme
  readOnly: true, // Read Only
  autoRefresh: true, // Allow for autorefresh
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
  isCodeExecuting.value = true;
  saveCode();
  let outputStore = "";
  // Remove previous output so there's no confusion
  outputResult.value = "";

  // First parameter is endpoint URL, second is header object
  let endpoint = import.meta.env.VITE_API_URL;
  let requestOptions = { 
    method: "POST",
    headers: { "auth-header": loginStore.token },
    body: JSON.stringify({ "code" : String(code.value) })
  }
  fetch(endpoint + "/execute/code", requestOptions)
    .then(async response => {
        const data = await response.json()

        console.log(data)

        if(response.ok) {
          let output = data["output"].trimEnd();
          outputStore = output;
          let error = data["error"];
          if (error != null && error.length > 0) {
            // Error case
            if(output.length > 0) {
              output += "\n";
            }
            output += error;
            showResultModal.value = true;
            showSuccessInResultModal.value = false;
            outputResult.value = output;
            isCodeExecuting.value = false;
          } else {
            // Success case
            executeCodeValidation(outputStore);
          }
        } else {
          // Error case
          showResultModal.value = true;
          showSuccessInResultModal.value = false;
          outputResult.value = data["detail"];
          isCodeExecuting.value = false;
        }
    })
}

function executeCodeValidation(outputStore) {
  let endpoint = import.meta.env.VITE_API_URL;
  const localStorageGptInfo = JSON.parse(localStorage.getItem(props.section.toString()));
  const localStorageGptRawResponse = localStorageGptInfo[props.id]["rawContent"];
  let validityRequestoptions = { 
    method: "POST",
    headers: { "auth-header": loginStore.token },
    body: JSON.stringify({
      "assistantMessage": localStorageGptRawResponse,
      "code" : String(code.value) 
    })
  }
  console.log(JSON.stringify(validityRequestoptions));
  fetch(endpoint + "/execute/code/validation", validityRequestoptions)
    .then(async response => {
      const data = await response.json();

      console.log(data);

      if(data["isValid"]) {
        showResultModal.value = true;
        showSuccessInResultModal.value = true;
        outputResult.value = outputStore;
        isCodeExecuting.value = false;
        pointsStore.updatePoints(1, props.section, props.id);
      } else {
        showResultModal.value = true;
        showSuccessInResultModal.value = false;
        pointsStore.updatePoints(0, props.section, props.id);
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

          <span class="col-span-2 text-right">
            <span class="ml-2 p-2 rounded-lg cursor-pointer transition-colors hover:border-gray-300 hover:bg-gray-100 hover:dark:border-neutral-700 hover:dark:bg-neutral-800/30" @click="decrementStep">
              <IconSvg name="angles-left" size="15px" class="inline"/>Prev
            </span>
            |
            <span class="p-2 rounded-lg cursor-pointer transition-colors hover:border-gray-300 hover:bg-gray-100 hover:dark:border-neutral-700 hover:dark:bg-neutral-800/30" @click="incrementStep">
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
        <div class="absolute top-0 right-0 z-10" title="Send Help!">
          <IconSvg class="bg-gray-600 rounded-full p-1.5 mt-1 mr-1 inline-block" name="info" size="30px" color="white" @click="showReferenceModal = true"/>
          <IconSvg class="bg-gray-600 rounded-full p-1.5 mt-1 mr-1 inline-block" name="lightbulb" size="30px" color="yellow" @click="showHintModal = true"/>
        </div>
        <div class="absolute bottom-0 right-0 z-10">
          <button class="bg-blue-400 rounded-lg font-bold text-l border-black border px-2.5 py-1 mb-1 mr-1" :disabled="isCodeExecuting" @click="saveCode">Save</button>
          <button class="bg-green-400 rounded-lg font-bold text-l border-black border px-2.5 py-1 mb-1 mr-1" :disabled="isCodeExecuting" @click="executeCode">Execute</button>
        </div>
      </div>

      <h2 class="mt-3">Output:</h2>
      <div class="relative h-[15vh]">
        <Codemirror
          v-model:value="outputResult"
          :options="cmReadOnlyOptionsOutput"
        />
        <VueSpinnerGears 
          v-if="isCodeExecuting === true"
          size="25" 
          color="orange"
          class="absolute bottom-2 right-2 z-10" 
        />
      </div>

      <!-- Build out reference modal in component to allow for per section customization -->
      <vue-final-modal
        v-bind="$attrs"
        v-model="showReferenceModal"
        classes="flex justify-center items-center"
        content-class="relative flex flex-col max-h-full w-3/5 mx-4 p-4 border dark:border-gray-800 rounded bg-white dark:bg-gray-900"
      >
        <TutorialReferenceSheet :section=section title="Reference Sheet"/>
        <button class="absolute top-0 right-0 mt-2 mr-2 p-2 rounded-lg hover:border-gray-300 hover:bg-gray-100 hover:dark:border-neutral-700 hover:dark:bg-neutral-800/30" @click="showReferenceModal = false">
          <IconSvg name="x" size="15px" />
        </button>
      </vue-final-modal>

      <vue-final-modal
        v-bind="$attrs"
        v-model="showHintModal"
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
        <button class="absolute top-0 right-0 mt-2 mr-2 p-2 rounded-lg hover:border-gray-300 hover:bg-gray-100 hover:dark:border-neutral-700 hover:dark:bg-neutral-800/30" @click="showHintModal = false">
          <IconSvg name="x" size="15px" />
        </button>
      </vue-final-modal>

      <Teleport to="body">
        <modal :show="showResultModal" :isSuccess="showSuccessInResultModal" @close="showResultModal = false"></modal>
      </Teleport>

  </div>
</template>
