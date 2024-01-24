import './index.css'

import { createApp } from 'vue'
import { createPinia } from 'pinia'

import icons from "v-svg-icons"
import VueWriter from "vue-writer"

import App from './App.vue'
import router from './router'

const app = createApp(App)

app.use(createPinia())
app.use(router)

app.component("IconSvg", icons)
app.component("VueWriter", VueWriter)

app.mount('#app')
