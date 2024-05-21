<template>
  <!-- 네비게이션 바 -->
  <nav class="navbar navbar-expand-lg navbar-light fixed-top">
    <div class="container-fluid">
      <RouterLink class="navbar-brand" :to="{ name: 'home' }">
        <img src="@/assets/logo.png" alt="logo_img" class="logo-img">
        <strong>PIGGY</strong>
      </RouterLink>
      <button
        class="navbar-toggler"
        type="button"
        data-bs-toggle="collapse"
        data-bs-target="#navbarNavDropdown"
        aria-controls="navbarNavDropdown"
        aria-expanded="false"
        aria-label="Toggle navigation"
      >
        <span class="navbar-toggler-icon"></span>
      </button>

      <div class="collapse navbar-collapse" id="navbarNavDropdown">
        <ul class="navbar-nav me-auto mb-2 mb-lg-0">
          <li v-if="authStore.isAuthenticated" class="nav-item">
            <RouterLink class="nav-link" :to="{ name: 'recommend', params: { username: authStore.userData.pk } }">
              상품 추천
            </RouterLink>
          </li>

          <li class="nav-item dropdown" @mouseover="showDropdown('product')" @mouseleave="hideDropdown('product')">
            <RouterLink
              class="nav-link dropdown-toggle"
              id="navbarDropdownMenuLink"
              role="button"
              :to="{ name: 'deposit' }"
            >
              상품 조회
            </RouterLink>
            <ul class="dropdown-menu" :class="{ show: dropdowns.product }" aria-labelledby="navbarDropdownMenuLink">
              <li>
                <RouterLink class="dropdown-item" :to="{ name: 'deposit' }">예금</RouterLink>
              </li>
              <li>
                <RouterLink class="dropdown-item" :to="{ name: 'savings' }">적금</RouterLink>
              </li>
              <li>
                <RouterLink class="dropdown-item" :to="{ name: 'loan' }">대출</RouterLink>
              </li>
            </ul>
          </li>

          <li class="nav-item dropdown" @mouseover="showDropdown('service')" @mouseleave="hideDropdown('service')">
            <RouterLink
              class="nav-link dropdown-toggle"
              id="navbarDropdownMenuLink"
              role="button"
              :to="{ name: 'exchange' }"
            >
              부가 서비스
            </RouterLink>
            <ul class="dropdown-menu" :class="{ show: dropdowns.service }" aria-labelledby="navbarDropdownMenuLink">
              <li>
                <RouterLink class="dropdown-item" :to="{ name: 'exchange' }">환율 조회</RouterLink>
              </li>
              <li>
                <RouterLink class="dropdown-item" :to="{ name: 'map' }">주변 은행 찾기</RouterLink>
              </li>
              <li>
                <RouterLink class="dropdown-item" :to="{ name: 'reTachInfo' }">재태크 정보</RouterLink>
              </li>
            </ul>
          </li>

          <li class="nav-item">
            <RouterLink class="nav-link" :to="{ name: 'community' }">커뮤니티</RouterLink>
          </li>
        </ul>
        <ul class="navbar-nav">
          <!-- 로그인된 경우 -->
          <li class="nav-item" v-if="authStore.isAuthenticated">
            <RouterLink :to="{ name: 'profile', params: { userId: authStore.userData.pk } }" class="nav-link"
              active-class="active-tab">
              프로필
            </RouterLink>
          </li>
          <li class="nav-item" v-if="authStore.isAuthenticated">
            <RouterLink :to="{ name: 'logout' }" class="nav-link" active-class="active-tab">
              로그아웃
            </RouterLink>
          </li>
          <!-- 로그인 안 된 경우 -->
          <li class="nav-item" v-if="!authStore.isAuthenticated">
            <RouterLink :to="{ name: 'login' }" class="nav-link" active-class="active-tab">
              로그인
            </RouterLink>
          </li>
          <li class="nav-item" v-if="!authStore.isAuthenticated">
            <RouterLink :to="{ name: 'signup' }" class="nav-link" active-class="active-tab">
              회원가입
            </RouterLink>
          </li>
        </ul>
      </div>
    </div>
  </nav>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from 'vue'
import { RouterLink } from 'vue-router'
import { useAuthStore } from '@/stores/auth'

const authStore = useAuthStore()

const dropdowns = ref({
  product: false,
  service: false
})

const showDropdown = (dropdown) => {
  dropdowns.value[dropdown] = true
}

const hideDropdown = (dropdown) => {
  dropdowns.value[dropdown] = false
}

const addScrollBorder = () => {
  const navbar = document.querySelector('nav')
  if (window.scrollY > 0) {
    navbar.classList.add('scroll-border')
  } else {
    navbar.classList.remove('scroll-border')
  }
}

onMounted(() => {
  window.addEventListener('scroll', addScrollBorder)
})

onUnmounted(() => {
  window.removeEventListener('scroll', addScrollBorder)
})
</script>

<style scoped>
nav {
  height: 80px; /* 높이 지정 */
  transition: border-bottom 0.3s ease; /* 스크롤 내릴 때 0.3초 뒤 바닥선 생김 */
  background-color: #f1f5ff; /* 네비바 지금 투명하게 적용되서 배경색 지정해줘야 함 */

  padding-right: 100px; /* 네비바도 #App이랑 똑같이 패딩 지정 */
  padding-left: 80px; /* 로고 이미지가 있어서그런지 넘 들어가 보여서 80px로 바꿈 */
}

nav.scroll-border {
  border-bottom: 2px solid #dee2e6; /* 바닥선 색깔 지정 */
}

.logo-img {
  height: 42px; /* 로고 크기 조정 */
  padding-bottom: 5px;
  margin-right: 10px; 
}

.navbar-nav .nav-link {
  color: #000;
  transition: color 0.3s ease, font-weight 0.3s ease;
}

.navbar-nav .nav-link:hover,
.navbar-nav .nav-link.active-tab {
  font-weight: bold; /* 글씨 굵게 */
  color: #000; /* 글씨 색 변경 안 되도록 설정 */
}

.dropdown-menu {
  display: none;
  /* background-color: #f1f5ff; 네비게이션 바와 동일한 배경색 */
  border: none; /* 테두리 제거 */
}

.dropdown-menu.show {
  display: block;
}

.dropdown-toggle::after {
  display: none; /* 드롭다운 화살표 제거 */
}

.dropdown-item {
  transition: font-weight 0.3s ease, background-color 0.3s ease;
  color: #000;
}

.dropdown-item:hover {
  font-weight: bold; /* 드롭다운 아이템 호버 시 글씨 굵게 */
  background-color: #e0e7ff; /* 연한 회색보다 약간 더 진한 색상 */
}
</style>
