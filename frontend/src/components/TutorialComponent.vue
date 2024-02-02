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
import { ref } from 'vue';
import { VueSpinner } from 'vue3-spinners';

const display = ref(1);
const content = ref([{}, {}, {}]);
const hasLoaded = ref(false);

const hasErrored = ref(false);
const errorMessage = ref("");

// First parameter is endpoint URL, second is header object
let baseUrl = import.meta.env.VITE_API_URL;
let endpoint = ""
if (import.meta.env.VITE_USE_LIVE_DATA == 'true') {
  endpoint = baseUrl + "?section=" + props.section + "&id=-1"
} else {
  endpoint = baseUrl + "/test"
}
fetch(endpoint, {})
    .then(async response => {
        const data = await response.json()

        console.log("Status: " + response.status + " - " + response.statusText)

        if(!response.ok) {
          console.log("There was an error!")
          console.log(data.detail)

          errorMessage.value = "There was an error loading data from OpenAI. Please reload the page."
          hasErrored.value = true;
        } else {
          const completions = data["completions"];
          for (var key in completions) {
            var index = Number(key)
            content.value[index-1] = completions[key];
          }
          hasLoaded.value = true;
        }
    })

function switchTab(id) {
  display.value = id;
}
</script>

<template>
    <main class="flex min-h-screen flex-col items-center justify-between p-24">
      <div class="z-10 max-w-6xl w-full items-center justify-between font-mono text-sm lg:flex">
        <div class="w-full">
          <!--
            The idea here is to have an unequal, 2-column layout.
            The left, smaller column will house a number of tabs to allow for navigation between exercises.
            The right, larger column will house the code editor.
          -->
          <div class="grid grid-cols-5 w-full">
            <div class="bg-transparent mr-5">
  
              <h1 class="font-bold text-2xl">
                {{ section }}
              </h1>
  
              <div v-for="exercise in exercises" :key="exercise.id">
                <TutorialTab :tabTitle=exercise.title @click="switchTab(exercise.id)" />
              </div>
  
            </div>
            <div v-if="hasLoaded" class="col-span-4">
  
              <div v-for="exercise in exercises" :key="exercise.id">
                <KeepAlive>
                  <TutorialContent v-if="display == exercise.id"
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
                <p class="font-bold font-xl text-red-500">Using the power of AI to generate a custom lesson plan just for you</p>
            </div>
          </div>
        </div>
      </div>
      <TutorialFooter />
    </main>
</template>

<style></style>