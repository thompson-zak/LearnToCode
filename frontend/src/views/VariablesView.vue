<script setup>
import TutorialTab from './../components/TutorialTab.vue'
import TutorialContent from './../components/TutorialContent.vue'
import TutorialFooter from './../components/TutorialFooter.vue'
import { ref } from 'vue';

const SECTION_DESCRIPTION = "These exercises are designed to help you understand the syntax of python and introduce you to the concept of variables."

const display = ref(1);
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

            <div>
              <TutorialTab tabTitle="Exercise 1" />
            </div>
            <div>
              <TutorialTab tabTitle="Exercise 2" />
            </div>
            <div>
              <TutorialTab tabTitle="Exercise 3" />
            </div>

          </div>
          <div class="col-span-4">

            <div>
              <TutorialContent v-if="display == 1"
                title="Exercise 1"
                :description=SECTION_DESCRIPTION
                gptPrompt="Please code something..."
                codeSkeleton="# Write your code for exercise 1 below."
                />
            </div>
            <div>
              <TutorialContent v-if="display == 2"
                title="Exercise 2"
                :description=SECTION_DESCRIPTION
                gptPrompt="Please code the volume of a cup of coffee."
                codeSkeleton="# Write your code for exercise 2 below."
                />
            </div>

            <div>
              <TutorialContent v-if="display == 3"
                title="Exercise 3"
                :description=SECTION_DESCRIPTION
                gptPrompt="Please code the temperature conversion from farenheit to celsius."
                codeSkeleton="# Write your code for exercise 3 below."
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
