<script setup>
import TutorialComponent from './../components/TutorialComponent.vue'

const sectionDescription = "These exercises are designed to help you understand the syntax of python and introduce you to the concept of variables."

const exercises = [
  {
    id: 1,
    listIndex: 0,
    section: "Variables",
    title: "Exercise 1"
  },
  {
    id: 2,
    listIndex: 1,
    section: "Variables",
    title: "Exercise 2"
  }
]
</script>

<template>
  <TutorialComponent :exercises=exercises :sectionDescription=sectionDescription />
</template>

<style>
</style>
