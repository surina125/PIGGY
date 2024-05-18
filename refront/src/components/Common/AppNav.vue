<template>
  <!-- 네비게이션 바 -->
  <nav class="navbar navbar-expand-lg navbar-light bg-light">
      <!-- 로그인된 경우 -->
      <RouterLink v-if="authStore.isAuthenticated" :to="{name: 'profile', params: {userId: authStore.userData.pk}}" class="nav-link"
        active-class="active-tab">
        프로필
      </RouterLink>
      <RouterLink v-if="authStore.isAuthenticated" :to="{name: 'logout'}" class="nav-link" active-class="active-tab">
        로그아웃
      </RouterLink>
      <!-- 로그인 안 된 경우 -->
      <RouterLink v-if="!authStore.isAuthenticated" :to="{name: 'login'}" class="nav-link" active-class="active-tab">
        로그인
      </RouterLink>
      <RouterLink v-if="!authStore.isAuthenticated" :to="{name: 'signup'}" class="nav-link" active-class="active-tab">
        회원가입
      </RouterLink>


    <div class="container-fluid">
      <RouterLink class="navbar-brand" :to="{name: 'home'}">PIGGY</RouterLink>
      <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNavDropdown" aria-controls="navbarNavDropdown" aria-expanded="false" aria-label="Toggle navigation">
        <span class="navbar-toggler-icon"></span>
      </button>

      <div class="collapse navbar-collapse" id="navbarNavDropdown">
        <ul class="navbar-nav">
          <li class="nav-item">
            <RouterLink v-if="authStore.isAuthenticated" class="nav-link" :to="{name: 'recommend', params: {username:  authStore.userData.pk}}">상품 추천</RouterLink>
          </li>

          <li class="nav-item dropdown">
            <RouterLink class="nav-link dropdown-toggle" id="navbarDropdownMenuLink" role="button" data-bs-toggle="dropdown" aria-expanded="false" :to="{name: 'deposit'}">상품 조회</RouterLink>
            <ul class="dropdown-menu" aria-labelledby="navbarDropdownMenuLink">
              <li>
                <RouterLink class="dropdown-item" :to="{name: 'deposit'}">예금</RouterLink>
              </li>
              <li>
                <RouterLink class="dropdown-item" :to="{name: 'savings'}">적금</RouterLink>
              </li>
              <li>
                <RouterLink class="dropdown-item" :to="{name: 'loan'}">대출</RouterLink>
              </li>
            </ul>
          </li>

          <li class="nav-item dropdown">
            <RouterLink class="nav-link dropdown-toggle" id="navbarDropdownMenuLink" role="button" data-bs-toggle="dropdown" aria-expanded="false" :to="{name: 'exchange'}">부가 서비스</RouterLink>
            <ul class="dropdown-menu" aria-labelledby="navbarDropdownMenuLink">
              <li>
                <RouterLink class="dropdown-item" :to="{name: 'exchange'}">환율 조회</RouterLink>
              </li>
              <li>
                <RouterLink class="dropdown-item" :to="{name: 'map'}">주변 은행 찾기</RouterLink>
              </li>
              <li>
                <RouterLink class="dropdown-item" :to="{name: 'reTachInfo'}">재태크 정보</RouterLink>
              </li>
            </ul>
          </li>

          <li class="nav-item">
            <RouterLink class="nav-link" :to="{name: 'community'}">커뮤니티</RouterLink>
          </li>
        </ul>
      </div>
    </div>
  </nav>

</template>

<script setup>
import { RouterLink } from 'vue-router'
import { useAuthStore } from '@/stores/auth'

const authStore = useAuthStore()

</script>

<style scoped>

</style>