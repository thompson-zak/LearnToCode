import { ref } from 'vue';
import { defineStore } from 'pinia';

export const useTrackStore = defineStore('track', () => {

    const track = ref(localStorage.getItem("userTrack") || "");

    function updateTrackStorage(newTrack) {
        localStorage.setItem("userTrack", newTrack);
    }

    function setTrack(newTrack) {
        track.value = newTrack;
        updateTrackStorage(newTrack);
    }

    return { track, setTrack }
})