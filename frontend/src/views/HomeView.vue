<script setup>
import { RouterLink } from 'vue-router';
import Modal from '../components/TracksModal.vue';
import { useTrackStore } from '@/stores/TrackStore';

const trackStore = useTrackStore();
</script>

<template>
  <main class="flex min-h-screen flex-col items-center justify-between p-24">
      <div class="z-10 max-w-5xl w-full items-center justify-between font-mono text-sm lg:flex">
        <p class="fixed left-0 top-0 flex w-full justify-center border-b border-gray-300 bg-gradient-to-b from-zinc-200 pb-6 pt-8 backdrop-blur-2xl dark:border-neutral-800 dark:bg-zinc-800/30 dark:from-inherit lg:static lg:w-auto  lg:rounded-xl lg:border lg:bg-gray-200 lg:p-4 lg:dark:bg-zinc-800/30">
          <code class="font-mono font-bold">Get started by selecting one of the sections below!</code>
        </p>
        <div class="fixed bottom-0 left-0 flex h-48 w-full items-end justify-center bg-gradient-to-t from-white via-white dark:from-black dark:via-black lg:static lg:h-auto lg:w-auto lg:bg-none rounded-lg border border-transparent px-4 py-3 transition-colors hover:border-gray-300 hover:bg-gray-100 hover:dark:border-neutral-700 hover:dark:bg-neutral-800/30">
          <a
            class="pointer-events-none flex place-items-center gap-2 p-8 lg:pointer-events-auto lg:p-0"
            href="https://www.markcubanai.org/"
            target="_blank"
            rel="noopener noreferrer"
          >
            <img src="../assets/cuban-logo.png" class="h-6"/>
          </a>
        </div>
      </div>

      <div class="relative flex place-items-center text-3xl font-bold">
        <vue-writer :array="['Learn To Code!']" class="text-4xl font-bold font-mono"/>
      </div>

      <div class="mb-32 grid text-center lg:max-w-5xl lg:w-full lg:mb-0 lg:grid-cols-4 lg:text-left">
        <RouterLink
          to="/tutorials/variables"
          class="group rounded-lg border border-transparent px-5 py-4 transition-colors hover:border-gray-300 hover:bg-gray-100 hover:dark:border-neutral-700 hover:dark:bg-neutral-800/30"
        >
          <span class="mb-3 text-2xl font-semibold inline-block">
            Variables
            <IconSvg name="arrow-right-long" size="25px" class="inline-block"></IconSvg>
          </span>
          <p class="m-0 max-w-[30ch] text-sm opacity-50">
            Learn about basic syntax and variables in this section, the building blocks of all code.
          </p>
        </RouterLink>

        <RouterLink
          to="/tutorials/data"
          class="group rounded-lg border border-transparent px-5 py-4 transition-colors hover:border-gray-300 hover:bg-gray-100 hover:dark:border-neutral-700 hover:dark:bg-neutral-800/30"
        >
        <span class="mb-3 text-2xl font-semibold inline-block">
            Data
            <IconSvg name="arrow-right-long" size="25px" class="inline-block"></IconSvg>
          </span>
          <p class="m-0 max-w-[30ch] text-sm opacity-50">
            Explore the many different types of data and the near unlimited ways you can store it.
          </p>
        </RouterLink>

        <RouterLink
          to="/tutorials/conditionals"
          class="group rounded-lg border border-transparent px-5 py-4 transition-colors hover:border-gray-300 hover:bg-gray-100 hover:dark:border-neutral-700 hover:dark:bg-neutral-800/30"
        >
        <span class="mb-3 text-2xl font-semibold inline-block">
            Conditionals
            <IconSvg name="arrow-right-long" size="25px" class="inline-block"></IconSvg>
          </span>
          <p class="m-0 max-w-[30ch] text-sm opacity-50">
            Try out ifs, elses, and elifs in order to make informed decisions based on all kinds of data.
          </p>
        </RouterLink>

        <RouterLink
          to="/tutorials/loops"
          class="group rounded-lg border border-transparent px-5 py-4 transition-colors hover:border-gray-300 hover:bg-gray-100 hover:dark:border-neutral-700 hover:dark:bg-neutral-800/30"
        >
        <span class="mb-3 text-2xl font-semibold inline-block">
            Loops
            <IconSvg name="arrow-right-long" size="25px" class="inline-block"></IconSvg>
          </span>
          <p class="m-0 max-w-[30ch] text-sm opacity-50">
            Dip your toe into loops, a core concept in any programming language.
          </p>
        </RouterLink>
      </div>
    </main>

    <Teleport to="body">
      <modal :show="trackStore.track === ''" @close="showTracksModal = false"></modal>
    </Teleport>
</template>

<style></style>
