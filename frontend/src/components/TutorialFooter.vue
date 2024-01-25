<script setup>
</script>

<template>
    <div class="max-w-6xl w-full mt-4">
      <RouterLink
        to="/"
        class="float-left group rounded-lg border border-transparent px-4 py-3 transition-colors hover:border-gray-300 hover:bg-gray-100 hover:dark:border-neutral-700 hover:dark:bg-neutral-800/30"
      >
        <h2 class="mb-2 text-2xl font-semibold">
          <IconSvg name="arrow-left-long" size="25px" class="inline-block"></IconSvg>
          Home
        </h2>
        <p class="m-0 max-w-[30ch] text-sm opacity-50 inline-block">
          Go back to start another lesson.
        </p>
      </RouterLink>

      <div class="float-right group rounded-lg border border-transparent px-4 py-3 transition-colors hover:border-gray-300 hover:bg-gray-100 hover:dark:border-neutral-700 hover:dark:bg-neutral-800/30">
        <a
          class="pointer-events-none flex place-items-center gap-2 p-8 lg:pointer-events-auto lg:p-0 inline-block"
          href="https://www.markcubanai.org/"
          target="_blank"
          rel="noopener noreferrer"
        >
          By
          <img src="../assets/cuban-logo.png" class="h-6 ml-2 inline-block"/>
        </a>
      </div>
    </div>
</template>

<style>
</style>