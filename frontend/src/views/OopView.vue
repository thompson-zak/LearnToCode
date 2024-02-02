<script setup>
import TutorialComponent from './../components/TutorialComponent.vue'

const section = "OOP"

const sectionDescription = "These exercises are designed to help you understand object-oriented programming, also known as OOP."

const exercises = [
  {
    id: 1,
    listIndex: 0,
    section: "OOP",
    title: "Exercise 1"
  },
  {
    id: 2,
    listIndex: 1,
    section: "OOP",
    title: "Exercise 2"
  }
]
</script>

<template>
  <TutorialComponent :exercises=exercises :section=section :sectionDescription=sectionDescription />
</template>

<style>
</style>