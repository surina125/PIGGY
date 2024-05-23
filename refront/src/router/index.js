import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '@/views/HomeView.vue'
import SearchView from '@/views/SearchView.vue'
import RecommendView from '@/views/RecommendView.vue'
import ServicesView from '@/views/ServicesView.vue'
import CommunityView from '@/views/CommunityView.vue'
import PostCreate from '@/components/Community/PostCreate.vue'
import PostDetail from '@/components/Community/PostDetail.vue'
import PostUpdate from '@/components/Community/PostUpdate.vue'

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
import ReTachPost1 from '@/components/Service/ReTachPost1.vue'
import ReTachPost2 from '@/components/Service/ReTachPost2.vue'

import Recommend2 from '@/components/Recommend/Recommend2.vue'
import twoResult from '@/components/Recommend/twoResult.vue'
import Deposit2 from '@/components/Recommend/Deposit2.vue'
import Saving2 from '@/components/Recommend/Saving2.vue'
import Loan2 from '@/components/Recommend/Loan2.vue'

import Recommend1 from '@/components/Recommend/Recommend1.vue'

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
      path: '/recommend/:username/one',
      name: 'one',
      component: Recommend1
    },
    {
      path: '/recommend/:username/two',
      name: 'two',
      component: Recommend2
    },
    {
      path: '/recommend/:username/two_result',
      component: twoResult,
      children: [
        {
          path: 'deposit2',
          name: 'deposit2',
          component: Deposit2
        },
        {
          path: 'saving2',
          name: 'saving2',
          component: Saving2
        },
        {
          path: 'loan2',
          name: 'loan2',
          component: Loan2
        },
      ]
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
        {
          path: 're_tack_info_post1',
          name: 'reTachPost1',
          component: ReTachPost1
        },
        {
          path: 're_tack_info_post2',
          name: 'reTachPost2',
          component: ReTachPost2
        },
      ]
    },
    {
      path: '/community',
      name: 'community',
      component: CommunityView,
     
    },
    {
      path: '/create',
      name: 'postcreate',
      component: PostCreate,
     
    },
    {
      path: '/detail/:postId',
      name: 'postdetail',
      component: PostDetail,

    },
    {
      path: '/update/:postId',
      name: 'postupdate',
      component: PostUpdate,
     
    },
    {
      path: '/signup',
      name: 'signup',
      component: SignUpView,
    },
    {
      path: '/login',
      name: 'login',
      component: LogInView,
    },
    {
      path: '/logout',
      name: 'logout',
      component: LogOutView
    },
    {
      path: '/profile/:userId',
      name: 'profile',
      component: ProfileView,
    },
    {
      path: '/update/:userId',
      name: 'info',
      component: UserInfo,
    },
  ]
})

export default router




