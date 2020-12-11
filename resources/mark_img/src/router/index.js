import Vue from 'vue'
import VueRouter from 'vue-router'

Vue.use(VueRouter)

const routes = [{
  path: '/',
  redirect: '/login'
}, 
{
  path: '/login',
  name: 'Login',
  component: () => import('@/views/login.vue')
},{
  path: '/register',
  name: 'Register',
  component: () => import('@/views/register.vue')
},{
  path: '/main',
  name: 'Main',
  component: () => import('@/components/common/Main.vue'),
  children: [
    {
      path: '/dataManage',
      name: 'DataManage',
      component: () => import( /* webpackChunkName: "about" */ '../views/data/dataManage.vue')
    },
    {
      path: '/markData',
      name: 'MarkData',
      // route level code-splitting
      // this generates a separate chunk (about.[hash].js) for this route
      // which is lazy-loaded when the route is visited.
      component: () => import( /* webpackChunkName: "about" */ '@/views/data/markData.vue')
    },
    {
      path: '/markImg/:id',
      name: 'MarkImg',
      // route level code-splitting
      // this generates a separate chunk (about.[hash].js) for this route
      // which is lazy-loaded when the route is visited.
      component: () => import( /* webpackChunkName: "about" */ '@/views/data/markImg.vue')
    }
  ]
}, ]

const router = new VueRouter({
  routes
})

export default router