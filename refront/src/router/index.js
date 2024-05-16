import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '@/views/HomeView.vue'
import SearchView from '@/views/SearchView.vue'
import RecommendView from '@/views/RecommendView.vue'
import ServicesView from '@/views/ServicesView.vue'
import CommunityView from '@/views/CommunityView.vue'


import Deposit from '@/components/Search/Deposit.vue'
import Savings from '@/components/Search/Savings.vue'
import Loan from '@/components/Search/Loan.vue'
import Exchange from '@/components/Service/Exchange.vue'
import Map from '@/components/Service/Map.vue'
import ReTachInfo from '@/components/Service/ReTachInfo.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: HomeView
    },
    {
      path: '/recommend/:username',
      name: 'recommend',
      component: RecommendView
    },
    {
      path: '/search',
      component: SearchView,
      children: [
        {
          path: 'deposit',
          name: 'deposit',
          component: Deposit
        },
        {
          path: 'savings',
          name: 'savings',
          component: Savings
        },
        {
          path: 'loan',
          name: 'loan',
          component: Loan
        },
      ]
    },
    {
      path: '/services',
      component: ServicesView,
      children: [
        {
          path: 'exchange',
          name: 'exchange',
          component: Exchange
        },
        {
          path: 'map',
          name: 'map',
          component: Map
        },
        {
          path: 're_tack_info',
          name: 'reTachInfo',
          component: ReTachInfo
        },
      ]
    },
    {
      path: '/community',
      name: 'community',
      component: CommunityView
    },
  ]
})

export default router
