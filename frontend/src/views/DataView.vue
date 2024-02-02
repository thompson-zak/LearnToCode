<script setup>
import TutorialComponent from './../components/TutorialComponent.vue'

const section = "Data"

const sectionDescription = "These exercises are designed to help you understand various essential data structures and how to use them."

const exercises = [
  {
    id: 1,
    listIndex: 0,
    section: "Data",
    title: "Exercise 1"
  },
  {
    id: 2,
    listIndex: 1,
    section: "Data",
    title: "Exercise 2"
  }
]
</script>

<template>
  <TutorialComponent :exercises=exercises :section=section :sectionDescription=sectionDescription />
</template>

<style>
</style>