<script setup>
import TutorialComponent from './../components/TutorialComponent.vue'

const section = "Loops"

const sectionDescription = "These exercises are designed to help you understand for and while loops."

const exercises = [
  {
    id: 1,
    listIndex: 0,
    section: "Loops",
    title: "Exercise 1"
  },
  {
    id: 2,
    listIndex: 1,
    section: "Loops",
    title: "Exercise 2"
  }
]
</script>

<template>
  <TutorialComponent :exercises=exercises :section=section :sectionDescription=sectionDescription />
</template>

<style>
</style>