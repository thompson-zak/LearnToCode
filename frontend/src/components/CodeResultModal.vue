<script setup>
const props = defineProps({
  show: Boolean,
  isSuccess: Boolean
})

const emit = defineEmits(['close']);

</script>

<template>
  <Transition name="modal">
    <div v-if="props.show" class="modal-mask">
      <div class="modal-container">
        <div class="modal-header">
          <slot name="header">Your code....</slot>
        </div>

        <div class="modal-body">
          <slot name="body">
            <p class="text-green-500" v-if="isSuccess">Has passed! Congrats, you've earned a point!</p>
            <p class="text-rose-500" v-else>Didn't quite solve the problem. Try again!</p>
          </slot>
        </div>

        <div class="modal-footer">
          <slot name="footer">
            <button
              class="modal-default-button rounded-lg border border-transparent px-3 py-2 transition-colors hover:border-gray-300 hover:bg-gray-100 hover:dark:border-neutral-700 hover:dark:bg-neutral-800/30"
              @click="emit('close')"
            >Continue</button>
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
  width: 400px;
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