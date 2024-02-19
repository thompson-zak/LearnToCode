<script setup>
// *** Code Mirror Dependencies *** //
import Codemirror from "codemirror-editor-vue3";
// language
import "codemirror/mode/python/python.js";
// placeholder
import "codemirror/addon/display/placeholder.js";
// autorefresh
import "codemirror/addon/display/autorefresh.js";
// theme
import "codemirror/theme/dracula.css";
// ******************************* //

const cmReadOnlyOptions = {
  mode: "text/x-python", // Language mode
  theme: "dracula", // Theme
  readOnly: true, // Read Only
  autoRefresh: true, // Allow for autorefresh
}

const exampleCode = "message = \"My favorite number is:\"\nfavoriteNumber = 9\nprint(message)\nprint(favoriteNumber)";
</script>

<template>
    <div class="mb-3">
        Python variables are simply containers for storing values. Python variables act as a placeholder in the computer's memory where you can put data.
        We'll look specifically at two types of data in this beginning section, strings and numbers.
    </div>
    <div class="mb-3">
        A string is any type of letter or word, which will be enclosed in double quotes (""). This is an easy way to store and represent text in your programs.
    </div>
    <div class="mb-3">
        A number is any combination of digits. Numbers can be super large or super small.
    </div>
    <div class="mb-3">
        Creating a varible is extremely simple and only requires you give the variable a name, something like 'message', and then assign a value using the equals sign.
        In our lessons we will be using a python functionality called "print". This will allow us to display the values of variables on screen within the output window.
    </div>
    <div class="mb-3">
        Here is a very basic example:
    </div>
    <Codemirror
          v-model:value="exampleCode"
          :options="cmReadOnlyOptions"
          class="mb-3"
    />
    <div class="mb-3">
        It's that simple! Now go and try it yourself!
    </div>
</template>

<style>
</style>