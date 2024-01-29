import './index.css'

import { createApp } from 'vue'
import { createPinia } from 'pinia'

import icons from "v-svg-icons"
import VueWriter from "vue-writer"
import { install as VueMonacoEditorPlugin } from '@guolao/vue-monaco-editor'
import { vfmPlugin } from 'vue-final-modal'

import App from './App.vue'
import router from './router'

const app = createApp(App)

app.use(createPinia())
app.use(router)
app.use(VueMonacoEditorPlugin , {
    paths: {
      // The recommended CDN config
      vs: 'https://cdn.jsdelivr.net/npm/monaco-editor@0.43.0/min/vs'
    },
})
app.use(vfmPlugin({
  key: '$vfm',
  componentName: 'VueFinalModal',
}))

app.component("IconSvg", icons)
app.component("VueWriter", VueWriter)

app.mount('#app')
