import Vue from 'vue'
import VueRouter from 'vue-router'
import Home from './views/Home.vue'

Vue.use(VueRouter)

const routes = [
  {
    path: '/',
    name: 'home',
    component: Home
  },
  {
    path: '/dashboard',
    name: 'dashboard',
    component: () => import('@/views/Dashboard.vue'),
    meta: {
      requiresAuth: true
    }
  },
  {
    path: '/form-detail/:id',
    name: 'form-detail',
    component: () => import('@/views/FormDetail.vue'),
    props: true
  },
  {
    path: '/form-create',
    name: 'form-create',
    component: () => import('@/views/FormCreate.vue')
  },
  {
    path: '/users/me',
    name: 'profile',
    component: () => import('@/views/User.vue')
  },
  {
    path: '/register',
    name: 'register',
    component: () => import('@/views/RegisterUser.vue')
  },
  {
    path: '/login',
    name: 'login',
    component: () => import('@/views/LoginUser.vue')
  },
  {
    path: '*',
    component: () => import('@/views/FileNotFound.vue')
  }
]

const router = new VueRouter({
  mode: 'history',
  routes
})

router.beforeEach((to, from, next) => {
  const loggedIn = localStorage.getItem('user')

  if (to.matched.some(record => record.meta.requiresAuth) && !loggedIn) {
    next('/')
  }
  next()
})

export default router
