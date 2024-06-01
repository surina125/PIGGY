<template>
  <div class="recommend1-page">
    <h3>설문조사 기반으로 추천받기</h3>
    <!-- 탭 -->
    <div class="nav-container mt-4 mb-4">
      <RouterLink 
        class="nav-card" 
        :class="{ active: $route.name === 'deposit2' }" 
        aria-current="page" 
        :to="{name: 'deposit2', params: {username: authStore.userData.username}}">
        <div class="nav-card-content">
          <h4>예금</h4>
          <p>안전한 예금 상품을 추천받으세요.</p>
        </div>
      </RouterLink>
      <RouterLink 
        class="nav-card" 
        :class="{ active: $route.name === 'saving2' }" 
        :to="{name: 'saving2', params: {username: authStore.userData.username}}">
        <div class="nav-card-content">
          <h4>적금</h4>
          <p>높은 이율의 적금 상품을 찾아보세요.</p>
        </div>
      </RouterLink>
      <RouterLink 
        class="nav-card" 
        :class="{ active: $route.name === 'loan2' }" 
        :to="{name: 'loan2', params: {username: authStore.userData.username}}">
        <div class="nav-card-content">
          <h4>주택담보대출</h4>
          <p>유리한 조건의 대출 상품을 확인하세요.</p>
        </div>
      </RouterLink>
    </div>

    <!-- 메인 -->
    <RouterView />
  </div>
</template>

<script setup>
import { useAuthStore } from '@/stores/auth';

const authStore = useAuthStore()
</script>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Roboto:wght@400;500;700&display=swap');

.recommend1-page {
  padding: 30px 100px;
  font-family: 'Roboto', sans-serif;
  color: #333;
  height: 100%;
  margin-bottom: 20%;
}

h3 {
  font-size: 24px;
  font-weight: 700;
  color: #333;
  margin-bottom: 20px;
  border-bottom: 2px solid #e0e0e0;
  padding-bottom: 10px;
}

.nav-container {
  display: flex;
  justify-content: space-around;
  margin-bottom: 20px;
}

.nav-card {
  background-color: #fff;
  padding: 20px;
  border-radius: 10px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
  text-decoration: none;
  color: #333;
  width: 30%;
  transition: transform 0.3s, box-shadow 0.3s, border 0.3s;
  border: 2px solid transparent;
}

.nav-card:hover {
  transform: translateY(-10px);
  box-shadow: 0 8px 16px rgba(0, 0, 0, 0.2);
}

.nav-card-content {
  text-align: center;
}

.nav-card h4 {
  font-size: 22px;
  font-weight: 700;
  margin-bottom: 10px;
}

.nav-card p {
  font-size: 16px;
  color: #555;
}

.nav-card.active {
  border: 4px solid #a89aaa;
  /* background-color: #f1f5ff; */
}
</style>
