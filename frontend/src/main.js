import './index.css'

import { createApp } from 'vue'
import { createPinia } from 'pinia'

import icons from "v-svg-icons"
import VueWriter from "vue-writer"
import { vfmPlugin } from 'vue-final-modal'
import { InstallCodemirro } from "codemirror-editor-vue3";

import App from './App.vue'
import router from './router'

const app = createApp(App)

app.use(InstallCodemirro)
app.use(createPinia())
app.use(router)
app.use(vfmPlugin({
  key: '$vfm',
  componentName: 'VueFinalModal',
}))

app.component("IconSvg", icons)
app.component("VueWriter", VueWriter)

app.mount('#app')
