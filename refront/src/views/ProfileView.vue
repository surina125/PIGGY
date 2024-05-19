<template>
  <div class="profile-container bg-light text-dark rounded mt-5 p-4">
    <div class="profile-pic-container mb-4 text-center">
      <img :src="userProfilePic" alt="프로필 이미지" class="profile-pic rounded-circle shadow" />
    </div>
    <div class="text-center mb-2">
      <h1>{{ authStore.userData.nickname }}님의 프로필</h1>
    </div>
    <div class="form-group">
      <label for="age">나이</label>
      <p>{{ authStore.userData.age }}</p>
    </div>
    <div class="form-group">
      <label for="annual_income">연간 소득</label>
      <p>{{ authStore.userData.annual_income }}</p>
    </div>
    <div class="form-group">
      <label for="property">자산</label>
      <p>{{ authStore.userData.property }}</p>
    </div>
    <div class="form-group">
      <label for="main_bank">주 은행</label>
      <p>{{ authStore.userData.main_bank }}</p>
    </div>
    <div class="form-group">
      <label for="saving_propensity">저축 성향</label>
      <p>{{ authStore.userData.saving_propensity }}</p>
    </div>
  </div>

  <RouterLink :to="{ name: 'userInfo', params: { userId: authStore.userData.pk }}">
    <h3>회원정보</h3>
  </RouterLink>

  <RouterView/>
</template>

<script setup>
import { useAuthStore } from '@/stores/auth'

const authStore = useAuthStore()

const userProfilePic = authStore.userData.profile_img ? `/media/${authStore.userData.profile_img}` : '/media/image/user.png';
</script>

<style scoped>
.profile-container {
  max-width: 500px;
  min-width: 300px;
  margin: 0 auto;
}

.profile-pic-container {
  position: relative;
}

.profile-pic {
  width: 150px;
  height: 150px;
  object-fit: cover;
}

.form-group {
  margin-bottom: 1rem;
}
</style>
