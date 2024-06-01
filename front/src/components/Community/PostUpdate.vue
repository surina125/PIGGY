
<template>
  <div class="container">
    <h2>게시글 수정</h2>
    <div class="form-container">
      <form @submit.prevent="handleSubmit">
        <div class="mb-3">
          <label for="title">제목</label>
          <input type="text" class="form-control" id="title" v-model="title" placeholder="제목을 입력해 주세요">
        </div>
        <div class="mb-3">
          <label for="content">내용</label>
          <textarea class="form-control" id="content" v-model="content" rows="5" placeholder="내용을 입력해 주세요"></textarea>
        </div>
        <button type="submit" class="btn btn-outline-dark" style="margin-right: 10px;">수정 완료</button>
        <button type="button" class="btn btn-outline-dark" @click="goPostDetail">수정 취소</button>
      </form>
    </div>
  </div>
</template>

<script setup>

import {ref} from 'vue'
import { useRouter } from 'vue-router'
import { usePostStore } from '@/stores/post'


const postStore = usePostStore()
const title = ref('')
const content = ref('')
const router = useRouter()

function handleSubmit() {
  const updateData = {
    title: title.value,
    content: content.value
  };
  
  postStore.postUpdate(postStore.detailInfos.id, updateData)
  .then(() => {
    router.push({
      name: 'postdetail',
      params: { postId: postStore.detailInfos.id }
    });
  })
  .catch((error) => {
    console.error(error);
  });
}

const goPostDetail = () => {
  router.back()

}
</script>

<style scoped>
.container {
  width: 70%; 
  margin: 0 auto; 
  padding-top: 20px;
}
h2 {
  margin-bottom: 20px;
}
.form-container {
  background-color: #fff;
  padding: 20px;
  box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
  border-radius: 8px;
}
.form-control {
  width: 100%;
  padding: 10px;
  margin-bottom: 15px;
  border: 1px solid #ccc;
  border-radius: 4px;
}

</style>