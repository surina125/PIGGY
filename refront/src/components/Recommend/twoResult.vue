<template>
  <div>
    <!-- 탭 -->
    <ul class="nav">
      <li class="nav-item">
        <RouterLink class="nav-link" aria-current="page" :to="{name: 'deposit2', params: {username: authStore.userData.username}}">예금</RouterLink>
      </li>
      <li class="nav-item">
        <RouterLink class="nav-link" :to="{name: 'saving2', params: {username: authStore.userData.username}}">적금</RouterLink>
      </li>
      <li class="nav-item">
        <!-- <RouterLink class="nav-link" :to="{name: 'loan2', params: {username: authStore.userData.username}}">대출</RouterLink> -->
      </li>
    </ul>

    <!-- 메인 -->
    <RouterView />
  </div>
</template>

<script setup>
import { useAuthStore } from '@/stores/auth';

const authStore = useAuthStore()

</script>

<style lang="scss" scoped>

</style>