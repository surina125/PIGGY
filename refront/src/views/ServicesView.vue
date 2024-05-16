<template>
  <div>
    <!-- 탭 -->
    <ul class="nav">
      <li class="nav-item">
        <RouterLink class="nav-link" aria-current="page" :to="{name: 'exchange'}">환율 조회</RouterLink>
      </li>
      <li class="nav-item">
        <RouterLink class="nav-link" :to="{name: 'map'}">주변 은행 찾기</RouterLink>
      </li>
      <li class="nav-item">
        <RouterLink class="nav-link" :to="{name: 'reTachInfo'}">재태크 정보</RouterLink>
      </li>
    </ul>

    <!-- 메인 -->
    <RouterView />
  </div>
</template>

<script setup>

</script>

<style scoped>

</style>