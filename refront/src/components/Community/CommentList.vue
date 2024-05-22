<template>
  <div>
    <h5>{{ postStore.commentInfos.length }}개의 댓글</h5>
    <hr>
    <div v-for="comment in postStore.commentInfos" :key="comment.id">
      <div v-if="editingCommentId === comment.id">
        <!-- 댓글 수정 폼 -->
        <form @submit.prevent="handleSubmitComment(comment.id)" class="commmiteditbox">
          <input type="text" v-model="editedCommentContent" class="form-control w-50">
          <div class="commentedit">
            <button type="submit" class="btn btn-outline-dark btn-sm" style="margin-right: 10px;">수정 완료</button>
            <button type="button" @click="cancelEdit" class="btn btn-outline-dark btn-sm">수정 취소</button>
          </div>
        </form>
      </div>
      <div v-else>
        <!-- 댓글 내용 표시 -->
        <span class="commentdetail">
          <p>작성자 : {{ comment.user.username }}</p>
          <p>{{ comment.created_at }}</p>
        </span>
        <span>{{ comment.content }}</span>
        <br>
        <span class="commentedit">
          <button class="btn btn-outline-dark btn-sm" v-if="authStore.userData.username === comment.user.username" @click="startEdit(comment.id)" style="margin-right: 10px;">댓글 수정</button>
          <button class="btn btn-outline-dark btn-sm" v-if="authStore.userData.username === comment.user.username" @click="commentDelete(comment.id)">댓글 삭제</button>
        </span>
      </div>
      <hr>
    </div>
  </div>
</template>

<script setup>
import { useAuthStore } from '@/stores/auth.js';
import { usePostStore } from '@/stores/post';
import { ref } from 'vue';
import { useRouter } from 'vue-router'

const authStore = useAuthStore();
const postStore = usePostStore();
const editingCommentId = ref(null);
const editedCommentContent = ref('');
const router = useRouter()
const postId = router.currentRoute.value.params.postId;

const startEdit = (commentId) => {
  editingCommentId.value = commentId;
  // 선택한 댓글의 내용을 수정 폼에 로드
  const comment = postStore.commentInfos.find(comment => comment.id === commentId);
  editedCommentContent.value = comment.content;
};

const cancelEdit = () => {
  editingCommentId.value = null;
  editedCommentContent.value = '';
};


function handleSubmitComment(commentId) {
  const updateData = {
    content: editedCommentContent.value
  };
 
  postStore.commentUpdate(postStore.detailInfos.id, commentId, updateData)
  .then(() => {
    editingCommentId.value = null,
    postStore.commentList(postId),
    router.push({
      name: 'postdetail',
      params: { postId: postStore.detailInfos.id }
    });
  })
  .catch((error) => {
    console.error(error);
  });
}

const commentDelete = (commentId) => {
  postStore.commentDelete(postId, commentId)
}
</script>

<style scoped>
.commentdetail {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.commmiteditbox {
  display: flex;
  justify-content: space-between;
}
.commentedit {
  display: flex;
  justify-content: flex-end;
  align-items: center;
}

</style>
