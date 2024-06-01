<template>
  <div class="table-container mt-4 community-page">
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
    <div class="writebox">    
      <RouterLink :to="{name:'postcreate'}">
        <button type="button" class="btn btn-outline-secondary" v-if="authStore.isAuthenticated" >글쓰기</button>
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
.table-container {
  height: 100%;
  padding: 50px;
  background-color: #ffffff;
  border: 1px solid #dee2e6;
  border-radius: 4px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  width: 70%;
  margin: 0 auto 200px auto;
}

h2 {
  text-align: center;
  margin-bottom: 20px;
  font-size: 24px;
  font-weight: bold;
}

.table {
  width: 100%;
  margin-bottom: 20px;
  border-collapse: collapse;
}

.table th, .table td {
  text-align: center;
  padding: 12px;
  border: 1px solid #dee2e6;
}

.table thead th {
  background-color: #f8f9fa;
  font-weight: bold;
}

.table-group-divider tr:hover {
  background-color: #f1f1f1;
  cursor: pointer;
}

.writebox {
  text-align: right;
  margin-top: 10px;
}

.btn {
  padding: 10px 20px;
  font-size: 16px;
  font-weight: bold;
  transition: background-color 0.3s, color 0.3s;
}

.btn-outline-secondary {
  color: #333;
  border-color: #333;
}

.btn-outline-secondary:hover {
  color: #fff;
  background-color: #333;
}
</style>
