<template>
  <div id="carouselExampleAutoplaying" class="carousel slide" data-bs-ride="carousel">
    <div class="carousel-inner">
      <div class="carousel-item active">
        <div class="box d-block w-100">
          <div class="carousel-container">
            <div class="carousel-box">
              <img class="carousel-image" src="@/assets/carousel1.png" alt="recommend_img">
              <div class="carousel-text">
                <h3 class="first-font">회원가입하고<br><strong>내게 딱─ 맞는</strong> 상품 찾기</h3>
                <p>PIGGY에서 추천 서비스를 이용해 보세요.</p>
                <button @click="handleRecommendationClick" class="recommend-link">
                  금융상품 추천받기
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>

      <div class="carousel-item">
        <div class="box d-block w-100">
          <div class="carousel-container">
            <div class="carousel-box second-carousel-box">
              <div class="carousel-text second-carousel-text">
                <h3 class="second-font"><span>예적금, 주택담보대출</span>을<br><strong>한 곳에 싹─ </strong>모아</h3>
                <p>PIGGY에서 편하게 금리비교 하세요.</p>
                <button @click="handleSearchClick" class="search-link">
                  금리 비교하기
                </button>
              </div>
              <img class="carousel-image" src="@/assets/carousel2.png" alt="search_img">
            </div>
          </div>
        </div>
      </div>
      <!-- 다른 캐러셀 아이템들 -->
      <!-- <div class="carousel-item">
        <img src="@/assets/carousel2.png" class="d-block w-100" alt="...">
      </div> -->
      <!-- 추가 캐러셀 아이템들 -->
    </div>
    <button class="carousel-control-prev" type="button" data-bs-target="#carouselExampleAutoplaying" data-bs-slide="prev">
      <span class="carousel-control-prev-icon" aria-hidden="true"></span>
      <span class="visually-hidden">Previous</span>
    </button>
    <button class="carousel-control-next" type="button" data-bs-target="#carouselExampleAutoplaying" data-bs-slide="next">
      <span class="carousel-control-next-icon" aria-hidden="true"></span>
      <span class="visually-hidden">Next</span>
    </button>
  </div>
</template>

<script setup>
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'

const authStore = useAuthStore()
const router = useRouter()

const handleRecommendationClick = () => {
  if (authStore.isAuthenticated) {
    router.push({ name: 'recommend', params: { username: authStore.userData.pk } })
  } else {
    router.push({ name: 'login' })
  }
}

const handleSearchClick = () => {
  router.push({ name: 'deposit' })
}
</script>

<style scoped>
.carousel-container {
  display: flex;
  justify-content: center;
  align-items: center;
  background-color: #f1f5ff; /* 원하는 배경색으로 변경 */
  padding: 20px;
}

.carousel-box {
  display: flex;
  align-items: center;
  width: 100%;
  max-width: 1200px;
  overflow: hidden;
  height: 70vh;
}

.carousel-box.second-carousel-box {
  justify-content: flex; 
  /* display: flex; */
  /* margin: auto; */
}

.carousel-image {
  width: auto;
  height: 100%;
}

.carousel-text {
  width: 50%;
  padding: 20px;
  font-family: 'Montserrat', sans-serif; /* Google Fonts 적용 */

.first-font {
  font-size: 40px; /* 텍스트 크기 조정 */
  margin-bottom: 20px;
  color: #333;
}
.second-font {
  font-size: 43px; /* 텍스트 크기 조정 */
  margin-bottom: 20px;
  color: #333;
}

 
p {
  font-size: 18px; /* 텍스트 크기 조정 */
  margin-bottom: 15px;
  color: #666; /* 회색상 */
}

.recommend-link, .search-link {
    display: inline-block;
    padding: 10px 20px;
    background-color: #007bff;
    color: #fff;
    font-size: 18px;
    font-weight: bold;
    text-decoration: none;
    border: none; /* button에 적합한 스타일로 변경 */
    border-radius: 5px;
    cursor: pointer; /* 클릭 가능 표시 */
    transition: background-color 0.3s ease;
  }

.recommend-link:hover, .search-link:hover {
    background-color: #0056b3;
  }
}

.second-carousel-text {
  text-align: right; /* 두 번째 카루셀 텍스트를 왼쪽 정렬 */
  margin-right: 40px;
}
</style>
