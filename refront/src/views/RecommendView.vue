<template>
  <div class="container">
    <div class="box" @click="navigateTo('one')">
      <h2>내 정보 기반으로 추천받기</h2>
      <p>프로필에 입력된 나이, 자산, 연봉을 기반으로 유사한 사람이 가입한 금융상품들을 추천해 드립니다.</p>
    </div>
    <div class="box" @click="navigateTo('two')">
      <h2>설문조사 기반으로 추천받기</h2>
      <p>원하는 상품 종류와 유형, 금리, 선호하는 은행을 선택하시면 이를 바탕으로 금융상품들을 추천해 드립니다.</p>
    </div>
    <button class="result-button" @click="navigateTo('deposit2')">결과 다시 보기</button>
  </div>
</template>

<script setup>
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import { useRecommendStore } from '@/stores/recommend'
import { onMounted } from 'vue'

onMounted(() => {
  const recommendStore = useRecommendStore()
  recommendStore.reco1D = [] // Initialize empty array for recommendations
  recommendStore.reco1S = []
  recommendStore.reco1L = []
  recommendStore.reco1Result()
})

const authStore = useAuthStore()
const router = useRouter()

const navigateTo = (page) => {
  if (page === 'one' && (authStore.userData.age === null || authStore.userData.annual_income === null || authStore.userData.property === null)) {
    router.push({ name: 'info', params: { username: authStore.userData.username } })
  } else {
    router.push({ name: page, params: { username: authStore.userData.username } })
  }
}
</script>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@400;700&display=swap');

html, body {
  height: 100%;
  margin: 0;
}

.container {
  display: flex;
  flex-direction: column;
  padding-top: 160px;
  /* justify-content: center; */
  align-items: center;
  width: 100vw;
  height: 100vh;
  background: #f1f5ff;
  font-family: 'Noto Sans KR', sans-serif;
}

.box {
  width: 100%;
  max-width: 600px;
  height: auto;
  background: #ffffff;
  border: 2px solid #333;
  color: #333;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  border-radius: 15px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
  transition: transform 0.3s, box-shadow 0.3s;
  cursor: pointer;
  text-align: center;
  padding: 40px;
  margin: 20px;
}

.box:hover {
  transform: translateY(-5px);
  box-shadow: 0 8px 16px rgba(0, 0, 0, 0.2);
}

h2 {
  margin: 0;
  font-size: 24px;
  font-weight: 700;
  color: #333;
}

p {
  margin: 20px 0 0;
  font-size: 18px;
  line-height: 1.6;
  color: #333;
}

.result-button {
  background-color: #333;
  color: white;
  border: none;
  padding: 15px 50px;
  font-size: 18px;
  border-radius: 30px;
  cursor: pointer;
  transition: background-color 0.3s, transform 0.3s;
  margin-top: 20px;
}

.result-button:hover {
  background-color: #555;
  transform: translateY(-5px);
}
</style>
