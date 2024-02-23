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

const exampleForCode = "for x in range(1, 10):\n\tprint(x)";
const exampleWhileCode = "x = 1\nwhile x <= 10:\n\tprint(x)\n\tx += 1";

</script>

<template>
    <div class="mb-3">
        In many cases, the problems you are looking to solve using code will require repeated operations. This is where the concept of loops comes in. A loop will perform an action or set of actions a certain
        number of times before reaching a terminating condition. The two types of loops we'll be examining are for loops and while loops, which are very similar but have some noticeable differences.
    </div>
    <h2 class="font-bold underline">For Loops</h2>
    <div class="mb-3">
        A for loop will iterate over a collection (such as an array) and execute the code within the block for every item in that collection.<br>
        Here is an example:
    </div>
    <Codemirror
          v-model:value="exampleForCode"
          :options="cmReadOnlyOptions"
          class="mb-3"
    />
    <h2 class="font-bold underline">While Loops</h2>
    <div class="mb-3">
        A while loops functions similarly to a for loop except that it will execute the code in the block as long as the condition given to it is true.<br>
    </div>
    <Codemirror
          v-model:value="exampleWhileCode"
          :options="cmReadOnlyOptions"
          class="mb-3"
    />
    <div class="mb-3">
        It's that simple! Now go and try it yourself!
    </div>
</template>

<style>
</style>