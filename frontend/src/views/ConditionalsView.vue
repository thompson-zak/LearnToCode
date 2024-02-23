<script setup>
import TutorialComponent from './../components/TutorialComponent.vue'

const section = "Conditionals"

const sectionDescription = "These exercises are designed to help you understand conditional statements - ifs, elses, and elifs."

const exercises = [
  {
    id: 1,
    listIndex: 0,
    section: "Conditionals",
    title: "Exercise 1"
  },
  {
    id: 2,
    listIndex: 1,
    section: "Conditionals",
    title: "Exercise 2"
  }
]
</script>

<template>
  <TutorialComponent :exercises=exercises :section=section :sectionDescription=sectionDescription />
</template>

<style>
</style>