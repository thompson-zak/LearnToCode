<script setup>
import { ref } from 'vue';
import { useLoginStore } from '@/stores/LoginStore'
import router from "@/router";

const userInput = ref("");
const loginStore = useLoginStore();
const errorMessage = ref("");

function attemptLogIn(){

    errorMessage.value = "";

    let endpoint = import.meta.env.VITE_API_URL;
    let requestOptions = {
        headers: { "auth-header" : userInput.value }
    }
    fetch(endpoint + "/login", requestOptions)
        .then(async response => {
            const data = await response.json()

            if(response.ok) {
                const token = data["token"];
                loginStore.setToken(token);
                userInput.value = "";
                router.push({ name: "home" })
            } else {
                loginStore.clearToken();
                errorMessage.value = "There was an issue logging you in. Please try again."
            }
        })
}
</script>

<template>
    <main class="flex min-h-screen flex-col items-center align-middle p-24">
        <div class="m-auto w-1/4">
            <div class="m-auto text-center">
                <span class="font-bold text-3xl font-mono mt-2 mr-4 h-40 align-middle">Hello, camper!</span>
                <IconSvg class="inline-block" name="hand" size="40px" color="#FFD300" />
            </div>
            <div class="m-auto pt-10">
                <input class="w-3/4 border rounded-tl-lg rounded-bl-lg p-2 font-mono" type="text" placeholder="Type your access code here..." v-model="userInput"/>
                <button class="w-1/4 border rounded-tr-lg rounded-br-lg bg-green-600 p-2 font-bold font-mono" @click="attemptLogIn">Submit</button>
            </div>
            <div class="m-auto text-center">
                <span class="text-rose-600 font-mono">{{ errorMessage }}</span>
            </div>
        </div>
    </main>
</template>

<style>
</style>