<template>
  <div class="container">
    <div class="content">
      <div class="image-container">
        <img src="@/assets/loanpost.png" class="main-image" alt="Main Image">
      </div>
      <div class="text-box">
      <h1 class="title">주택담보대출, 금리 낮은 상품은 따로 있어요</h1>
      <div class="text">
        주택담보대출(이하 주담대)의 금리가 오르는 추세예요. 그 이유와 함께 금리가 낮은 주담대 상품을 찾는 팁을 알려드릴게요.
      </div>
      <hr>
      <h2 class="subtitle">주담대 금리가 오르는 이유</h2>
      <div class="text">
        주담대 금리가 오르는 가장 큰 이유로는 정부의 가계대출 억제 방침이 꼽혀요. 금융 당국이 올해 3월부터 가계대출 증가 속도를 늦추기 위해 나섰거든요.
        그 때문에 은행들은 금융 당국에 올해 연간 가계대출 증가율을 2% 내로 관리하겠다고 보고했어요. 신생아 특례대출 이용자가 빠르게 느는 등 가계대출이 늘고 있어서, 가계대출 수요를 낮추려면 결국 금리를 올리는 수밖에 없어요.
      </div>
      <hr>
      <h2 class="subtitle">금리가 낮은 주담대는 없을까?</h2>
      <div class="text">
        먼저 주담대의 대출금 상환 방식은 크게 고정형과 변동형으로 나뉘어요. 그중 고정형은 다시 혼합형과 주기형으로 나뉘고요.
      </div>
      <ul class="text">
        <li>변동형: 일반적으로 6개월마다 대출금리가 바뀌는 방식</li>
        <li>혼합형: 초기 3년이나 5년은 고정금리를 적용하고 이후에는 6개월 단위로 금리가 바뀌는 방식</li>
        <li>주기형: 5년 단위로 고정금리가 갱신되는 방식</li>
      </ul>
      <div class="text">
        주기형 주담대의 장점이자 단점은 금리 변동기에에도 등락이 없다는 거예요. 5년 이내에 금리가 인상되어도 금리변동이 없지만, 금리가 떨어져도 내 금리에는 변동이 없어요.
        그런데 금융당국이 최근 은행권에 주담대 중 고정형이나 주기형의 비중을 30% 이상으로 맞춰달라고 주문했어요. 시장 상황이 불투명하니 고정금리 확대를 유도하는 거예요. 그 때문에 주기형의 금리가 더 저렴하게 조정될 것이라는 관측이 나와요.
      </div>
    </div>
  </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
</script>

<style scoped>
.text-box {
  padding-right: 40px;
  padding-left: 40px;
}

.container {
  font-family: Arial, sans-serif;
  padding: 20px;
  max-width: 800px;
  margin: 0 auto;
  background-color: #f9f9f9;
  border-radius: 10px;
  box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
}

.content {
  margin-top: 20px;
  padding-right: 20px;
  padding-left: 20px;
}

.image-container {
  text-align: center;
  margin-bottom: 30px;
}

.main-image {
  max-width: 100%;
  height: auto;
  border-radius: 10px;
}

.title {
  font-size: 24px;
  margin-top: 50px;
  margin-bottom: 40px;
  font-weight: bold;
  text-align: center;
  color: #333;
}

.text {
  font-size: 16px;
  margin-bottom: 20px;
  color: #555;
  line-height: 2;
}

.subtitle {
  font-size: 18px;
  margin-top: 30px;
  margin-bottom: 15px;
  font-weight: bold;
  color: #333;
}

ul.text {
  list-style-type: disc;
  margin-left: 20px;
  color: #555;
}

@media (max-width: 600px) {
  .container {
    padding: 15px;
  }
  .title {
    font-size: 20px;
  }
  .text {
    font-size: 14px;
  }
  .subtitle {
    font-size: 16px;
  }
}
</style>
