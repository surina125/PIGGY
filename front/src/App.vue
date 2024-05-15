<template>
  <div>
    <header>
      <Nav></Nav>
      <div class="hr"></div>
    </header>
    <main>
      <RouterView />
      <!-- <Footer class="footer"/>  -->
    </main>
  </div>
</template>

<script setup>
import Nav from '@/components/Nav.vue'
import Footer from '@/components/Footer.vue'

window.addEventListener('scroll', function() {
  const header = document.querySelector('header');
  
  // 스크롤 위치 확인
  if (window.scrollY > 0) {
    header.style.borderBottom = '1px solid #ccc'
  } else {
    header.style.borderBottom = '1px solid transparent'
  }
});
</script>

<style scoped>
header {
  background-color: #f1f5ff;
  position: fixed; 
  top: 0;
  left: 0;
  width: 100%;
  z-index: 1000; 
}


main {
  padding-top: 81px;
}

/* 
.footer {
  /* position: absolute;
  bottom: -200px; */
  /* position: relative;
  bottom: -150px;
  transform : translateY(100%);
} */ 
</style>


