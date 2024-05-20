
<template>
  <div>
    <h1>게시물</h1>
    <p>제목: {{ postStore.detailInfos.title }}</p>
    <p>내용 : {{ postStore.detailInfos.content }}</p>

    <button v-if="authStore.userData.username === postStore.detailInfos.user.username" @click="postUpdate(postStore.detailInfos.id)">게시물 수정</button> 
    <button v-if="authStore.userData.username === postStore.detailInfos.user.username" @click="postStore.postDelete(postStore.detailInfos.id)">게시물 삭제</button>  

    <hr>

    <div v-if="authStore.isAuthenticated">
      <form @submit.prevent="createComment">
        <label for="comment">댓글</label>
        <input type="text" id="comment" v-model="commentText"/>
        <button type="submit">댓글 생성</button>
      </form>
      <hr>
    </div>

    <div>
      <CommentList />
    </div>
  </div>
</template>

<script setup>
import { useRouter } from 'vue-router';
import { ref, onMounted } from 'vue';
import { useAuthStore } from '@/stores/auth.js';
import { usePostStore } from '@/stores/post';
import CommentList from '@/components/Community/CommentList.vue';

const authStore = useAuthStore();
const postStore = usePostStore();
const router = useRouter();
const commentText = ref("");


const postId = router.currentRoute.value.params.postId;

const postUpdate = (postId) => {
  router.push({ name: 'postupdate', params: { postId: postId } });
}

const createComment = () => {
  postStore.commentCreate(postId, commentText.value);
  commentText.value = "";
}


onMounted( () => {
  postStore.postDetail(postId);
  // postStore.commentList(postId);
  
});


</script>
