<script setup>
defineProps({
  exercises: {
    type: Object,
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
import { ref } from 'vue';
import { VueSpinner } from 'vue3-spinners';

const display = ref(1);
const content = ref("");
const hasLoaded = ref(false);

// First parameter is endpoint URL, second is header object
// TODO - error handling
let endpoint = import.meta.env.VITE_API_URL;
fetch(endpoint + "/test", {})
    .then(response => response.json())
    .then(data => {
        console.log(data);
        content.value = data;
        hasLoaded.value = true;
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
                Variables
              </h1>
  
              <div v-for="exercise in exercises" :key="exercise.id">
                <TutorialTab :tabTitle=exercise.title @click="switchTab(exercise.id)" />
              </div>
  
            </div>
            <div v-if="hasLoaded" class="col-span-4">
  
              <div v-for="exercise in exercises" :key="exercise.id">
                <TutorialContent v-if="display == exercise.id"
                  :title=exercise.title
                  :description=sectionDescription
                  :userPrompt=exercise.userPrompt
                  :gptContent=content
                />
              </div>
              
            </div>

            <div v-else class="col-span-4 auto-rows-max h-[70vh] flex flex-col items-center justify-center">
                <VueSpinner size="40" color="red"/>
                <div class="h-5"></div>
                <p>Using the power of AI to generate a custom lesson plan just for you</p>
            </div>
          </div>
        </div>
      </div>
      <TutorialFooter />
    </main>
</template>

<style></style>