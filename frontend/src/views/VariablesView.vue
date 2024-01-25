<script setup>
import TutorialTab from './../components/TutorialTab.vue'
import TutorialContent from './../components/TutorialContent.vue'
import TutorialFooter from './../components/TutorialFooter.vue'
import { ref } from 'vue';

const SECTION_DESCRIPTION = "These exercises are designed to help you understand the syntax of python and introduce you to the concept of variables."

const display = ref(1);

const tabs = [
  {
    id: 1,
    title: "Exercise 1"
  },
  {
    id: 2,
    title: "Exercise 2"
  },
  {
    id: 3,
    title: "Exercise 3"
  }
]

const exercises = [
  {
    id: 1,
    section: "Variables",
    title: "Exercise 1",
    userPrompt: "Please code something..."
  },
  {
    id: 2,
    section: "Variables",
    title: "Exercise 2",
    userPrompt: "Please code the volume of a cup of coffee."
  },
  {
    id: 3,
    section: "Variables",
    title: "Exercise 3",
    userPrompt: "Please code the temperature conversion from farenheit to celsius."
  }
]

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

            <div v-for="tab in tabs" :key="tab.id">
              <TutorialTab :tabTitle=tab.title @click="switchTab(tab.id)" />
            </div>

          </div>
          <div class="col-span-4">

            <div v-for="exercise in exercises" :key="exercise.id">
              <TutorialContent v-if="display == exercise.id"
                :title=exercise.title
                :description=SECTION_DESCRIPTION
                :user-prompt=exercise.userPrompt
              />
            </div>
            
          </div>
        </div>
      </div>
    </div>
    <TutorialFooter />
  </main>
</template>

<style>
</style>
