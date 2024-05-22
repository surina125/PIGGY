<template>
  <div class="table-container">
    <h2>금융상품 추천 게시판</h2>
    <table class="table">
      <thead>
        <tr>
          <th scope="col">No.</th>
          <th scope="col">제목</th>
          <th scope="col">글쓴이</th>
          <th scope="col">작성시간</th>
        </tr>
      </thead>
      <tbody class="table-group-divider">
        <tr v-for="(post,index) in postStore.postInfos" :key="post.id" @click="goDetail(post.id)">
          <th scope="row">{{index+1}}</th>
          <td>{{ post.title }}</td>
          <td>{{ post.user.username}}</td>
          <td>{{ post.formatted_created_at }}</td>
        </tr>
      </tbody>
    </table>
    <div>    
      <RouterLink :to="{name:'postcreate'}">
        <div class="writebox">
          <button type="button" class="btn btn-outline-secondary" v-if="authStore.isAuthenticated" >글쓰기</button>
        </div>
      </RouterLink>
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

h2{
  margin-bottom: 20px;
}
.table-container {
  width: 70%; 
  margin: 0 auto; 
}
.writebox {
  text-align: right;

}
</style>
