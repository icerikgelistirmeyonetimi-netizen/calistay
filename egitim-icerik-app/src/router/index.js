import { createRouter, createWebHashHistory } from 'vue-router'
import HomePage from '../views/HomePage.vue'
import DersDetay from '../views/DersDetay.vue'
import TurYonetimi from '../views/TurYonetimi.vue'

const router = createRouter({
  history: createWebHashHistory(),
  routes: [
    {
      path: '/',
      name: 'home',
      component: HomePage
    },
    {
      path: '/ders/:dersAdi',
      name: 'dersDetay',
      component: DersDetay,
      props: true
    },
    {
      path: '/tur-yonetimi',
      name: 'turYonetimi',
      component: TurYonetimi
    }
  ]
})

export default router
