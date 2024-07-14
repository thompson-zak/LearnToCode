<script setup>
import Multiselect from 'vue-multiselect';
import { ref } from 'vue';
import { useTrackStore } from '@/stores/TrackStore';

const props = defineProps({
  show: Boolean
})

const emit = defineEmits(['close']);

const options = ref(['Sports Science', 'Business', 'Arts & Entertainment', 'Computer Science', 'Education', 'Healthcare']);
const selectedTrack = ref('');
const showError = ref(false);
const trackStore = useTrackStore();

function onSelect() {
    if (selectedTrack.value !== '') {
        trackStore.setTrack(selectedTrack.value);
        showError.value = false;
        emit('close')
    } else {
        showError.value = true;
    }
}
</script>

<template>
  <Transition name="modal">
    <div v-if="props.show" class="modal-mask">
      <div class="modal-container">
        <div class="modal-header">
          <slot name="header">Before we start, what track are you interested in?</slot>
        </div>

        <div class="modal-body">
          <slot name="body">
            <multiselect v-model="selectedTrack" :options="options" :searchable="false" :close-on-select="true" :show-labels="false" placeholder="Pick a track!"></multiselect>
          </slot>
        </div>

        <div class="modal-footer">
          <slot name="footer">
            <button
              class="modal-default-button rounded-lg border border-transparent px-5 py-4 transition-colors hover:border-gray-300 hover:bg-gray-100 hover:dark:border-neutral-700 hover:dark:bg-neutral-800/30"
              @click="onSelect"
            >Lock in my track!</button>
            <p v-if="showError" class="text-rose-500">Please select a track before continuing.</p>
          </slot>
        </div>
      </div>
    </div>
  </Transition>
</template>

<style src="vue-multiselect/dist/vue-multiselect.esm.css"></style>
<style>
.modal-mask {
  position: fixed;
  z-index: 9998;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0, 0, 0, 0.5);
  display: flex;
  transition: opacity 0.3s ease;
}

.modal-container {
  width: 550px;
  margin: auto;
  padding: 20px 30px;
  background-color: #fff;
  border-radius: 2px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.33);
  transition: all 0.3s ease;
}

.modal-header {
  margin-top: 0;
  color: black;
  font-weight: 500;
}

.modal-body {
  margin: 20px 0;
}

.modal-default-button {
  float: right;
}

/*
 * The following styles are auto-applied to elements with
 * transition="modal" when their visibility is toggled
 * by Vue.js.
 *
 * You can easily play with the modal transition by editing
 * these styles.
 */

.modal-enter-from {
  opacity: 0;
}

.modal-leave-to {
  opacity: 0;
}

.modal-enter-from .modal-container,
.modal-leave-to .modal-container {
  -webkit-transform: scale(1.1);
  transform: scale(1.1);
}
</style>