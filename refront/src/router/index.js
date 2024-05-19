import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '@/views/HomeView.vue'
import SearchView from '@/views/SearchView.vue'
import RecommendView from '@/views/RecommendView.vue'
import ServicesView from '@/views/ServicesView.vue'
import CommunityView from '@/views/CommunityView.vue'
import PostCreate from '@/components/Community/PostCreate.vue'

import SignUpView from '@/views/SignUpView.vue'
import LogInView from '@/views/LogInView.vue'
import LogOutView from '@/views/LogOutView.vue'
import ProfileView from '@/views/ProfileView.vue'
import UserInfo from '@/components/User/UserInfo.vue'

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
      component: CommunityView,
      children : [
        {
          path: 'create',
          name: 'postcreate',
          component: PostCreate

        }

      ]
    },
    {
      path: '/signup',
      name: 'signup',
      component: SignUpView,
      // beforeEnter: (to, from) => {
      //   const store = useAuthStore()
      //   if (store.isAuthenticated) {
      //     return { name: 'home' }
      //   }
      // }
    },
    {
      path: '/login',
      name: 'login',
      component: LogInView,
      // beforeEnter: (to, from) => {
      //   const store = useAuthStore()
      //   if (store.isAuthenticated) {
      //     return { name: 'home' }
      //   }
      // }
    },
    {
      path: '/logout',
      name: 'logout',
      component: LogOutView
    },
    {
      path: '/user/profile/:userId',
      name: 'profile',
      component: ProfileView,
      children: [
        { path: 'info', name: 'userInfo', component: UserInfo },
      ]
    },
  ]
})

export default router
