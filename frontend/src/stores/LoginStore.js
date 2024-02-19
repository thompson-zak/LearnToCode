import { ref } from 'vue'
import { defineStore } from 'pinia'
import router from "@/router";

export const useLoginStore = defineStore('login', () => {
    
    const isLoggedIn = ref(localStorage.getItem("isLoggedIn") == "true");
    const token = ref(localStorage.getItem("userToken") || "");

    function updateLogInStorage(logInStatus) {
        localStorage.setItem("isLoggedIn", logInStatus);
    }

    function logIn() {
        isLoggedIn.value = true;
        updateLogInStorage(true);
    }

    function logOut() {
        isLoggedIn.value = false;
        updateLogInStorage(false);
    }

    function updateTokenStorage(newToken) {
        localStorage.setItem("userToken", newToken);
    }

    function setToken(newToken) {
        token.value = newToken;
        updateTokenStorage(newToken);
        logIn();
    }

    function clearToken() {
        token.value = "";
        updateTokenStorage("");
        logOut();
        router.push({ name: "login" })
    }

    function checkTokenStatus() {

        // If token is not present, ensure log in state is set to false
        if(token.value == "" || token.value == null) {
            return;
        }
            
        let endpoint = import.meta.env.VITE_API_URL;
        let requestOptions = {
            headers: { "auth-header" : token.value }
        }
        console.log(requestOptions)
        fetch(endpoint + "/checkToken", requestOptions)
            .then(async response => {
                const data = await response.json()

                console.log(data)

                if(response.ok) {
                    const isValid = data["valid"];
                    if(!isValid) {
                        clearToken();
                    }
                } else {
                    console.log("There was an issue validating your token.");
                    clearToken();
                }
            })
    }
  
    return { isLoggedIn, token, logIn, logOut, setToken, clearToken, checkTokenStatus }
  })