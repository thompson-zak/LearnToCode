<script setup>
const props = defineProps({
  exercises: {
    type: Object,
    required: true
  },
  section: {
    type: String,
    required: true
  },
  sectionDescription: {
    type: String,
    required: true
  }
})

import TutorialTab from './../components/TutorialTab.vue'
import TutorialContent from './../components/TutorialContent.vue'
import TutorialFooter from './../components/TutorialFooter.vue'
import TutorialLoadingSlideshow from './TutorialLoadingSlideshow.vue';
import TutorialReferenceSheet from './reference/TutorialReferenceSheet.vue';
import { ref } from 'vue';
import { VueSpinner } from 'vue3-spinners';
import { useLoginStore } from '@/stores/LoginStore';

const loginStore = useLoginStore();

// Show modal only if they have never seen it before. Closing from this screen will store a value, indicating the page has been visited.
const showReferenceModal = ref(localStorage.getItem(props.section + "Modal") == null || localStorage.getItem(props.section + "Modal") == "")

const display = ref(1);
const content = ref([{}, {}, {}]);
const hasLoaded = ref(false);

const hasErrored = ref(false);
const errorMessage = ref("");

getComponentData();

function closeModal() {
  showReferenceModal.value = false;
  localStorage.setItem(props.section + "Modal", "false")
}

function getComponentData() {
  const storedData = getLocalStorage();
  const cacheData = import.meta.env.VITE_CACHE_DATA;

  if(storedData != null) {
    populateContent(JSON.parse(storedData));
    hasLoaded.value = true;
  } else {
    getOpenAiData().then(completions => {
      if(completions != null && cacheData == 'true') {
        setLocalStorage(completions);
      }
    })
  }
}

function getOpenAiData() {
  // First parameter is endpoint URL, second is header object
  let baseUrl = import.meta.env.VITE_API_URL;
  let endpoint = ""
  if (import.meta.env.VITE_USE_LIVE_DATA == 'true') {
    endpoint = baseUrl + "?section=" + props.section + "&id=-1"
  } else {
    endpoint = baseUrl + "/test"
  }
  let requestOptions = { 
    headers: { "auth-header": loginStore.token }
  }
  return fetch(endpoint, requestOptions)
      .then(async response => {
          const data = await response.json()

          if(!response.ok) {
            errorMessage.value = "There was an error loading data from OpenAI. Please reload the page.";
            hasErrored.value = true;
            Promise.reject();
          } else {
            const completions = data["completions"];
            populateContent(completions);
            hasLoaded.value = true;
            return completions;
          }
      })
      .catch(() => {
        errorMessage.value = "There was an error loading data from OpenAI. Please reload the page.";
        hasErrored.value = true;
        Promise.reject();
      })
}

function populateContent(completions) {
  for (var key in completions) {
    var index = Number(key)
    content.value[index-1] = completions[key];
  }
}

function switchTab(id) {
  display.value = id;
}

function getLocalStorage() {
  return localStorage.getItem(props.section)
}

function setLocalStorage(item) {
  localStorage.setItem(props.section, JSON.stringify(item))
}
</script>

<template>
    <main v-if="showReferenceModal" class="flex min-h-screen flex-col items-center justify-between px-24 pb-12 pt-20">
      <div class="w-1/2 m-auto">
        <TutorialReferenceSheet :section=section title="Introduction"/>
        <div class="w-full text-center mt-3">
          <button class="p-3 bg-green-500 rounded-lg" @click="closeModal">Got it!</button>
        </div>
      </div>
    </main>
    <main v-else class="flex min-h-screen flex-col items-center justify-between px-24 pb-12 pt-20">
      <div class="z-10 max-w-6xl w-full items-center justify-between font-mono text-sm lg:flex">
        <div class="w-full">
          <!--
            The idea here is to have an unequal, 2-column layout.
            The left, smaller column will house a number of tabs to allow for navigation between exercises.
            The right, larger column will house the code editor.
          -->
          <div class="grid grid-cols-5 w-full">
            <div class="bg-transparent mr-5 flex flex-1 flex-col justify-between">
  
              <div>
                <h1 class="font-bold text-2xl">
                  {{ section }}
                </h1>
    
                <div v-for="exercise in exercises" :key="exercise.id">
                  <TutorialTab :tabTitle=exercise.title @click="switchTab(exercise.id)" />
                </div>
              </div>

              <RouterLink
                to="/"
                class="align-bottom group rounded-lg border border-transparent px-4 py-3 transition-colors hover:border-gray-300 hover:bg-gray-100 hover:dark:border-neutral-700 hover:dark:bg-neutral-800/30"
              >
                <h2 class="mb-2 text-2xl font-semibold">
                  <IconSvg name="arrow-left-long" size="25px" class="inline-block"></IconSvg>
                  Home
                </h2>
                <p class="m-0 max-w-[30ch] text-sm opacity-50 inline-block">
                  Go back to start another lesson.
                </p>
              </RouterLink>
  
            </div>
            <div v-if="hasLoaded" class="col-span-4">
  
              <div v-for="exercise in exercises" :key="exercise.id">
                <KeepAlive>
                  <TutorialContent v-if="display == exercise.id"
                    :section=section
                    :title=exercise.title
                    :description=sectionDescription
                    :content=content[exercise.listIndex]
                  />
                </KeepAlive>
              </div>
              
            </div>

            <div v-if="hasLoaded === false && hasErrored === false" class="col-span-4 auto-rows-max h-[70vh] flex flex-col items-center justify-center">
                <VueSpinner size="40" color="red"/>
                <div class="h-5"></div>
                <TutorialLoadingSlideshow />
            </div>

            <div v-if="hasErrored" class="col-span-4 auto-rows-max h-[70vh] flex flex-col items-center justify-center">
                <p class="font-bold font-xl text-red-500">{{ errorMessage }}</p>
            </div>
          </div>
        </div>
      </div>

      <TutorialFooter />
    </main>
</template>

<style></style>