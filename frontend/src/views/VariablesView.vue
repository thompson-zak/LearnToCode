<script setup>
import TutorialTab from './../components/TutorialTab.vue'
import TutorialContent from './../components/TutorialContent.vue'
</script>

<template>
  <main class="flex min-h-screen flex-col items-center justify-between p-24">
        <div class="z-10 max-w-6xl w-full items-center justify-between font-mono text-sm lg:flex">
          <div class="w-full">
      <div class="w-full">
        <h1 class="float-left font-bold text-2xl">
          Variables
        </h1>
        <div class="float-right">
            <a
              class="pointer-events-none flex place-items-center gap-2 p-8 lg:pointer-events-auto lg:p-0"
              href="https://www.markcubanai.org/"
              target="_blank"
              rel="noopener noreferrer"
            >
              By
              <a>
                <img src="../assets/cuban-logo.png" class="h-6 ml-2"/>
              </a>
            </a>
          </div>
      </div>
      
      <!--
        The idea here is to have an unequal, 2-column layout.
        The left, smaller column will house a number of tabs to allow for navigation between exercises.
        The right, larger column will house the code editor.
      -->
      <div class="grid grid-cols-5 w-full">
        <div class="bg-transparent mr-5">

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
            <TutorialContent 
              title="Exercise 1"
              description={sectionDescription}
              gptPrompt="Please code something..."
              codeSkeleton="# Write your code for exercise 1 below."
              />
          </div>
          <div>
            <TutorialContent 
              title="Exercise 2"
              description={sectionDescription}
              gptPrompt="Please code the volume of a cup of coffee."
              codeSkeleton="# Write your code for exercise 2 below."
              />
          </div>

          <div>
            <TutorialContent 
              title="Exercise 3"
              description={sectionDescription}
              gptPrompt="Please code the temperature conversion from farenheit to celsius."
              codeSkeleton="# Write your code for exercise 3 below."
              />
          </div>
        </div>
      </div>
    </div>
        </div>
        <div class="max-w-6xl w-full mt-4">
          <a
            href="/"
            class="float-left group rounded-lg border border-transparent px-4 py-3 transition-colors hover:border-gray-300 hover:bg-gray-100 hover:dark:border-neutral-700 hover:dark:bg-neutral-800/30"
          >
            <h2 class="mb-3 text-2xl font-semibold">
              <IconSvg name="arrow-left-long" size="25px" class="inline-block"></IconSvg>
              Home
            </h2>
            <p class="m-0 max-w-[30ch] text-sm opacity-50 inline-block">
              Go back to start another lesson.
            </p>
          </a>
        </div>
    </main>
</template>

<style>
</style>
