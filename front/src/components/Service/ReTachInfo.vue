<template>
  <div class="container">
    <div class="card-row">
      <div class="card mb-3" @click="goToPost1">
        <div class="row g-0 h-100">
          <div class="col-md-4 h-100">
            <img src="@/assets/retechpig.webp" class="img-fluid rounded-start w-100 h-100" alt="적금 이미지">
          </div>
          <div class="col-md-8">
            <div class="card-body h-100 d-flex flex-column justify-content-center text-center">
              <div>
                <h5 class="card-title cardtitlebold">적금 잘 활용하는 5가지 방법</h5>
                <hr>
                <p class="card-text">적금 들기 전에 알면 도움이 되는 5가지 팁을 소개할게요.</p>
              </div>
            </div>
          </div>
        </div>
      </div>
      <div class="card mb-3" @click="goToPost2">
        <div class="row g-0 h-100">
          <div class="col-md-4 h-100">
            <img src="@/assets/house.png" class="img-fluid rounded-start w-100 h-100" alt="주택 이미지">
          </div>
          <div class="col-md-8">
            <div class="card-body h-100 d-flex flex-column justify-content-center text-center">
              <div>
                <h5 class="card-title cardtitlebold">주택담보대출, 금리 낮은 상품 찾기</h5>
                <hr>
                <p class="card-text p-2">금리가 낮은 주담대 상품을 찾는 팁을 알려드릴께요</p>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
    <div class="card-row">
      <div class="card mb-3">
        <div class="row g-0 h-100">
          <div class="col-md-4 h-100">
            <img src="@/assets/fan.webp" class="img-fluid rounded-start w-100 h-100" >
          </div>
          <div class="col-md-8">
            <div class="card-body h-100 d-flex flex-column justify-content-center text-center">
              <div>
                <h5 class="card-title cardtitlebold">월세처럼 매달 통장에 돈이 들어오는 '적금 풍차돌리기'</h5>
                <hr>
                <p class="card-text p-2">금리가 빠르게 오르면서 적금 풍차돌리기 재테크가 다시 떠오르는 중이예요</p>
              </div>
            </div>
          </div>
        </div>
      </div>
      <div class="card mb-3">
        <div class="row g-0 h-100">
          <div class="col-md-4 h-100">
            <img src="@/assets/price.png" class="img-fluid rounded-start w-100 h-100" alt="부동산 이미지">
          </div>
          <div class="col-md-8">
            <div class="card-body h-100 d-flex flex-column justify-content-center text-center">
              <div>
                <h5 class="card-title cardtitlebold">전세vs월세vs매매, 뭐가 좋을까?</h5>
                <hr>
                <p class="card-text p-2">지역과 주택유형에 따라 부동산 가격이 천차만별인데, 어떤 차이가 있는지 설명해드릴게요</p>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
    <div class="card-row">
      <div class="card mb-3">
        <div class="row g-0 h-100">
          <div class="col-md-4 h-100">
            <img src="@/assets/saving.png" class="img-fluid rounded-start w-100 h-100" alt="예적금 이미지">
          </div>
          <div class="col-md-8">
            <div class="card-body h-100 d-flex flex-column justify-content-center text-center">
              <div>
                <h5 class="card-title cardtitlebold">장기 예적금에 주목하는 이유</h5>
                <hr>
                <p class="card-text p-2">금리가 높으니 만기 1년 상품에 올인해도 될까요?</p>
              </div>
            </div>
          </div>
        </div>
      </div>
      <div class="card mb-3">
        <div class="row g-0 h-100">
          <div class="col-md-4 h-100">
            <img src="@/assets/house1.webp" class="img-fluid rounded-start w-100 h-100" >
          </div>
          <div class="col-md-8">
            <div class="card-body h-100 d-flex flex-column justify-content-center text-center">
              <div>
                <h5 class="card-title cardtitlebold">2024년 달라지는 청약제도 4가지</h5>
                <hr>
                <p class="card-text p-2">올해 3월부터 청약제도가 대대적으로 달라져요. 어떤 점이 달라지는지 알려드릴께요.</p>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { useRouter } from 'vue-router';
const router = useRouter();

const goToPost1 = () => {
  router.push({ name: 'reTachPost1' });
};

const goToPost2 = () => {
  router.push({ name: 'reTachPost2' });
};
</script>

<style scoped>
.cardtitlebold {
  font-weight: bold;
  text-align: center;
  font-size: 1.5rem; /* 글자 크기를 키움 */
  white-space: nowrap; /* 제목이 한 줄로 나오게 설정 */
  overflow: hidden;
  text-overflow: ellipsis;
}

.card {
  height: 300px; /* 카드 높이를 키움 */
  flex: 0 0 calc(48% - 10px); /* 카드가 2개씩 배치되도록 너비를 설정 */
  margin: 5px; /* 카드 사이의 간격을 설정 */
  background-color: #f8f9fa;
  border: 1px solid #e0e0e0;
  border-radius: 10px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
  transition: transform 0.2s, box-shadow 0.2s;
}

.card:hover {
  transform: translateY(-5px);
  box-shadow: 0 8px 16px rgba(0, 0, 0, 0.2);
}

.card-body {
  padding: 20px;
  text-align: center;
  display: flex;
  flex-direction: column;
  justify-content: center;
}

.card h5 {
  font-size: 1.5rem; /* 글자 크기를 키움 */
}

.card p {
  font-size: 1.1rem; /* 글자 크기를 키움 */
}

.img-fluid {
  object-fit: cover;
  height: 100%;
  width: 100%;
  border-top-left-radius: 10px;
  border-bottom-left-radius: 10px;
}

.container {
  max-width: 1140px;
  margin: 20px auto;
}

.card-row {
  display: flex;
  flex-wrap: wrap;
  justify-content: space-between;
}

@media (max-width: 768px) {
  .card {
    flex: 0 0 100%; /* 작은 화면에서는 카드가 한 줄에 하나씩 배치되도록 설정 */
  }
}
</style>
