<template>
  <div>
    <div>
      <Carousel/>
    </div>


    <div v-if="authStore.isAuthenticated" class="recoResult">
      <RecoResult/>
    </div>

    <div v-if="authStore.isAuthenticated">
      <div class="mt-5 mb-5">
        <h3 class="text-center mt-5">주변 은행 찾기</h3>
        <Map/>
      </div>

      <div class="exchange-page mt-5 mb-5">
        <h3 class="text-center mt-5">환율 계산기</h3>
        <Exchange/>
      </div>
    </div>

    <!-- 로그인안했을경우에는 색이 바뀌게 하기 위해 순서 바꿔줌 -->
    <div v-else>
      <div class="exchange-page mt-5 mb-5">
        <h3 class="text-center mt-5">환율 계산기</h3>
        <Exchange/>
      </div>
      <div class="mt-5 mb-5">
        <h3 class="text-center mt-5">주변 은행 찾기</h3>
        <Map/>
      </div>

    </div>
  </div>
</template>

<script setup>
import Carousel from '@/components/MainPage/Carousel.vue'
import RecoResult from '@/components/MainPage/RecoResult.vue'
import Map from '@/components/Service/Map.vue'
import Exchange from '@/components/Service/Exchange.vue'
import { useAuthStore } from '@/stores/auth'

const authStore = useAuthStore()
</script>

<style scoped>
/* .recoResult {
  width: 100%;
} */

.exchange-page {
  width: 100%;
  padding-top: 7px;
  background-color: white;
}

</style>