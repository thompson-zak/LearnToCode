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

const exampleIfCode = "# If\na = 10\nb = 1\nif a > b :\n\tprint(\"A is bigger than B.\")";
const exampleIfElseElifCode = "# If/Elif/Else\na = 10\nb = 1\nif a > b :\n\tprint(\"A is bigger than B.\")\nelif b > a :\n\tprint(\"B is bigger than A.\")\nelse:\n\tprint(\"A and B are the same.\")";

</script>

<template>
    <div class="mb-3">
        Python has a variety of logical conditions which allow you to compare values. For this lesson we'll be looking at an important few:<br>
        &emsp;&emsp;Equals: a == b<br>
        &emsp;&emsp;Not Equals: a != b<br>
        &emsp;&emsp;Less than: a &lt; b<br>
        &emsp;&emsp;Less than or equal to: a &lt;= b<br>
        &emsp;&emsp;Greater than: a &gt; b<br>
        &emsp;&emsp;Greater than or equal to: a &gt;= b<br>
    </div>
    <h2 class="font-bold underline">If Statements</h2>
    <div class="mb-3">
        An if statement in Python is just a way to make a decision based on this comparison. If the statement is true, then the code within the if block will execute.
    </div>
    <Codemirror
          v-model:value="exampleIfCode"
          :options="cmReadOnlyOptions"
          class="mb-3"
    />
    <h2 class="font-bold underline">Elif and Else</h2>
    <div class="mb-3">
        We can do more with this, as there are some extensions to if statements that are useful. These are the elif and else. An elif is just another chained if statement that will be evaluated
        if the previous if statement was determined to be false. An else statement is a way to run some code if every other if is false. Here's an example:
    </div>
    <Codemirror
          v-model:value="exampleIfElseElifCode"
          :options="cmReadOnlyOptions"
          class="mb-3"
    />
    <div class="mb-3">
        It's that simple! Now go and try it yourself!
    </div>
</template>

<style>
</style>