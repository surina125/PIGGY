<template>
  <div>
    <h1>게시글 목록 페이지</h1>

      <RouterLink :to="{name:'postcreate'}">
        <button v-if="authStore.isAuthenticated">게시글 생성</button>
      </RouterLink>
    <div v-for="(post,index) in postStore.postInfos" :key="post.id" @click="goDetail(post.id)">
      <p>{{index+1}} - {{ post.title }}</p>
    </div>
  </div>
</template>

<script setup>
import { RouterLink } from 'vue-router'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth.js'
import { usePostStore } from '@/stores/post'


const router = useRouter()
const authStore = useAuthStore()
const postStore = usePostStore()


postStore.postList()

const goDetail = (pk) => {
  router.push({name:'postdetail', params:{postId: pk}})
  
}
</script>

<style scoped>
/* 스타일링 */
</style>