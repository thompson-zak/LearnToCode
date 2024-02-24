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

const exampleArrayCode = "fruits = [\"Apple\", \"Banana\", \"Strawberry\"]\nprint(fruits)";
const exampleDictionaryCode = "fruitCounts = {\n\t\"Apple\": 8,\n\t\"Banana\": 3,\n\t\"Strawberry\": 5\n}\nprint(fruitCounts)";

</script>

<template>
    <div class="mb-3">
        As we learned in the previous lesson, variables are stores of data. You also learned about strings and numbers. In this lesson we'll be learning about containers that
        can store many different values at once. These are called collections and we'll be taking a look at two types, arrays and dictionaries.
    </div>
    <h2 class="font-bold underline">Arrays</h2>
    <div class="mb-3">
        An array can be thought of as a list of values which have an order, can be changed, and allows for duplicates. You can access each of these stored values by their index,
        which begins at [0] and ends at [length - 1]. For most programming languages, all list indices will start at 0. Remember this so you start at the right place!
    </div>
    <Codemirror
          v-model:value="exampleArrayCode"
          :options="cmReadOnlyOptions"
          class="mb-3"
    />
    <h2 class="font-bold underline">Dictioinaries</h2>
    <div class="mb-3">
        A dictionary is similar to an array, except that it does not store it's contents with index:value pairs but rather with key:value pairs. A key is a string that tells the computer
        where to look for the corresponding value. Due to this, dictionaries do not allow for duplicate keys.
    </div>
    <Codemirror
          v-model:value="exampleDictionaryCode"
          :options="cmReadOnlyOptions"
          class="mb-3"
    />
    <div class="mb-3">
        It's that simple! Now go and try it yourself!
    </div>
</template>

<style>
</style>