import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'
import LoginView from '../views/LoginView.vue'
import { useLoginStore } from '@/stores/LoginStore'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: HomeView
    },
    {
      path: '/login',
      name: 'login',
      component: LoginView
    },
    {
      path: '/tutorials/variables',
      name: 'variables',
      // route level code-splitting
      // this generates a separate chunk (About.[hash].js) for this route
      // which is lazy-loaded when the route is visited.
      component: () => import('../views/VariablesView.vue')
    },
    {
      path: '/tutorials/data',
      name: 'data',
      // route level code-splitting
      // this generates a separate chunk (About.[hash].js) for this route
      // which is lazy-loaded when the route is visited.
      component: () => import('../views/DataView.vue')
    },
    {
      path: '/tutorials/conditionals',
      name: 'conditionals',
      // route level code-splitting
      // this generates a separate chunk (About.[hash].js) for this route
      // which is lazy-loaded when the route is visited.
      component: () => import('../views/ConditionalsView.vue')
    },
    {
      path: '/tutorials/oop',
      name: 'oop',
      // route level code-splitting
      // this generates a separate chunk (About.[hash].js) for this route
      // which is lazy-loaded when the route is visited.
      component: () => import('../views/OopView.vue')
    },
  ]
})

router.beforeEach((to) => {
  
  const loginStore = useLoginStore();

  loginStore.checkTokenStatus();

  console.log(loginStore.token);

  if (to.name !== 'login' && !loginStore.isLoggedIn) {
    return { name: 'login' }
  }

  if (to.name == 'login' && loginStore.isLoggedIn) {
    return { name: 'home' }
  }
})

export default router
