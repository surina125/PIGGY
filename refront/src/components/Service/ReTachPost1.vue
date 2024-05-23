<template>
  <div class="container">
    <div class="image-container">
      <img src="@/assets/savingpost.png" class="main-image" alt="Main Image">
    </div>
    <div class="content">
      <div class="text-box">
        <h1 class="title">적금을 잘 활용하는 5가지 방법</h1>
        
        <div class="text">
          적금은 일정 기간 돈을 저축하고, 약속한 기간이 지나면 원금과 이자를 한꺼번에 돌려받는 금융 상품이에요. 예금자 보호도 되는 데다 한번 가입하면 돈을 꺼내 쓰기 번거로워 사회 초년생들이 종잣돈을 모으는 데 적합해요.
          <br><br>
          요즘은 금리가 오르면서, 이자 수익도 꽤 쏠쏠하답니다.
          <br><br>
          그런데, 적금도 다 같은 적금이 아니라는 거 아시나요? 이율은 물론 납입 방식, 납입 금액, 가입 기간 등 세부 조건에 따라 나에게 더 유리한 적금을 선택할 수 있어요. 적금 잘 활용하는 5가지 방법을 소개할게요.
        </div>
        <hr>
        <div class="item" v-for="item in items" :key="item.id">
          <div class="info">
            <div class="title">{{ item.title }}</div>
            <div class="text" v-html="item.text"></div>
          </div>
          <hr v-if="!isLastItem(item.id)">
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'

const items = ref([
  {
    id: 1,
    title: "1. 납입 방식 확인하기 : 정기 적금 vs 자유 적금",
    text: `
      적금은 저축 주기에 따라 두 가지로 나뉘어요. 
      매달 정해진 날짜마다 일정 금액을 넣는 정기 적금과 돈이 생길 때마다 편하게 저금하는 자유 적금이 있어요. 
      매달 급여를 받는 직장인이라면 정기적금, 소득이 불규칙한 프리랜서나 사업자라면 자유 적금이 편할 수 있겠죠?`,
  },
  {
    id: 2,
    title: "2. 저축 한도 확인하기",
    text: `
      적금 상품 가입할 때 이율만큼 중요한 게 있어요. 바로 월 최대 납부 금액인데요.
      은행에서 신규 고객을 대상으로 낮은 기본 금리에 추가 우대 금리를 제공하는 특판(특별판매) 적금의 경우,
      월 최대 납입 가능 금액이 30만 원, 50만 원 등으로 낮게 설정된 경우가 있어요.
      이자가 아무리 높아도, 저금할 수 있는 금액이 작으면 우리의 이자 소득도 줄어들겠죠?`,
  },
  {
    id: 3,
    title: "3. 적금 가입 기간 확인하기",
    text: `
      한국은행에서 정한 규정에 따르면 적금의 최소 가입 기간은 1년의 절반인 6개월이에요. 
      그래서 보통 은행에서는 6개월 만기, 1년 만기, 2년 만기 등의 적금 상품을 취급하죠.
      보통 가입 기간이 길수록 은행 입장에서는 고객 돈을 더 오래 보관하고 사용(운용)할 수 있기 때문에, 적금 금리도 높아요.
      하지만 요즘 같은 금리 인상기에는 적금 가입 기간이 짧을수록 유리할 수 있어요. 
      기준 금리가 오르면서 더 높은 이율, 더 높은 조건의 적금 상품이 나올 수도 있거든요.`,
  },
  {
    id: 4,
    title: "4. 중도해지 이율 확인하기",
    text: `
      더 좋은 상품이 나오면 그때 갈아타면 되지 않냐고요? 
      적금을 중도에 해지하면 원금은 돌려받을 수 있지만, 사전에 약속된 이자를 다 받을 수 없어요. 
      가입 기간에 따라 다르긴 하지만, 계약할 때보다 낮은 중도해지 금리가 적용되어요. 
      이율이 높더라도 중도 해지하는 것보다 처음부터 만기가 짧은 상품에 가입해 약속된 이자를 다 받는 것이 나은 건 아닌지 확인해보세요.`,
  },
  {
    id: 5,
    title: "5. 우대 금리 조건 확인하기",
    text: `
      높은 금리를 내세우는 적금 상품이라도 내가 실제로 받을 수 있는 금리는 얼마인지 확인해야 해요. 
      최고 금리를 받으려면 신규 계좌 개설, 카드 발급, 실적 충족, 마이데이터 사용 동의, 인터넷 뱅킹 사용, 급여 및 공과금 자동 이체 등 여러 조건을 동시에 만족해야 할 수도 있거든요.`,
  },
])

const isLastItem = (id) => {
  return id === items.value[items.value.length - 1].id;
}
</script>

<style scoped>
.container {
  font-family: Arial, sans-serif;
  padding: 20px;
  max-width: 800px;
  margin: 0 auto;
  background-color: #f9f9f9;
  border-radius: 10px;
  box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
}
.title {
  font-size: 24px;
  margin-top: 50px;
  margin-bottom: 40px;
  font-weight: bold;
  text-align: center;
  color: #333;
}
.content {
  margin-top: 20px;
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

.text-box {
  padding-right: 40px;
  padding-left: 40px;
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

hr {
  border: none;
  border-top: 1px solid black;
  margin: 20px 0;
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
