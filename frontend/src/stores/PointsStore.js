import { ref } from 'vue';
import { defineStore } from 'pinia';

export const usePointsStore = defineStore('points', () => {

    const points = ref({
        "Variables": {
            1: localStorage.getItem("Variables1Points") || 0,
            2: localStorage.getItem("Variables2Points") || 0
        },
        "Data": {
            1: localStorage.getItem("Data1Points") || 0,
            2: localStorage.getItem("Data2Points") || 0
        },
        "Conditionals": {
            1: localStorage.getItem("Conditionals1Points") || 0,
            2: localStorage.getItem("Conditionals2Points") || 0
        },
        "Loops": {
            1: localStorage.getItem("Loops1Points") || 0,
            2: localStorage.getItem("Loops2Points") || 0
        }
    })

    function updatePoints(newPoints, section, id) {
        points.value[section][id] = newPoints;
        const localStorageKey = section + id.toString() + 'Points'; 
        localStorage.setItem(localStorageKey, newPoints);
    }

    function getPoints(section, id) {
        return points.value[section][id];
    }

    function getPointsTotal() {
        let total = 0;
        // eslint-disable-next-line no-unused-vars
        for (const [sectionKey, sectionValue] of Object.entries(points.value)) { 
            // eslint-disable-next-line no-unused-vars
            for (const [pointsKey, pointsValue] of Object.entries(sectionValue)) { 
                total += pointsValue;
            }
        }
        return total;
    }

    return { points, updatePoints, getPoints, getPointsTotal }

})