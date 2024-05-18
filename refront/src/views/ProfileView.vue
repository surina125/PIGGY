<template>
  <div>
    000님
    <RouterLink :to="{ name: 'userInfo', params: { userId: authStore.userData.pk }}">
      <h3>회원정보</h3>
    </RouterLink>

    <RouterView/>
  </div>
</template>

<script setup>
import { RouterLink } from 'vue-router'
import { useAuthStore } from '@/stores/auth'

const authStore = useAuthStore()
</script>

<style scoped>

</style>
