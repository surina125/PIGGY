import { ref, computed } from 'vue'
import { defineStore } from 'pinia'
import { useRouter } from 'vue-router'
import axios from 'axios'
import { useAuthStore } from './auth'

export const usePostStore = defineStore('post', () => {



  const router = useRouter()
  const authStore = useAuthStore()
  const postInfos = ref({})
  const detailInfos = ref({})
  const commentInfos = ref({})

  const postList = function() {
    axios.get('http://127.0.0.1:8000/community/post/')
    .then(response => {
      postInfos.value = response.data
    })
    .catch(error => {
      console.log(error)
    })
    
  }

  const postDetail = function (postId) {
    return axios({
      method:'get',
      url:`http://127.0.0.1:8000/community/post/${postId}/`,
    })
    .then((response) => {
      detailInfos.value = response.data
    })
    .catch((error)=>{
      console.log(error)
    })
  }
  


const postUpdate = function(postId, updateData) {
  return axios({
    method : 'put',
    url : `http://127.0.0.1:8000/community/post/${postId}/edit/`,
    headers: {
      'Authorization': `Token ${authStore.token}`
    },
    data : updateData
  })
  .then((response) => {
    return response.data;
    
  })
  .catch((error) => {
    console.log(error);
    throw error;
  });
};


 const postDelete = function(postId) {
  axios({
    method:'delete',
    url:`http://127.0.0.1:8000/community/post/${postId}/edit/`,
    headers: {
      'Authorization': `Token ${authStore.token}`
    },
  })
  .then((response) => {
    router.push({name:'community'})
    
  })
  .catch((error)=>{
    console.log(error)
  })

}

const commentCreate = function(post_pk, comment, updateData) {
  axios({
    method:'post',
    url:`http://127.0.0.1:8000/community/post/${post_pk}/comment/create/`,
    headers: {
      'Authorization': `Token ${authStore.token}`
    },
    data: {
      content: comment
    }
  })
  .then((response) => {
   commentList(post_pk)
    
  })
  .catch((error) => {
    console.log(error)
  })

}


const commentList = function(post_pk) {
  axios({
    method:'get',
    url:`http://127.0.0.1:8000/community/post/${post_pk}/comment/`,
  })
  .then((response) => {
    commentInfos.value = response.data
    console.log(commentInfos.value )
    

  })
  .catch((error) => {
    console.log(error)

  })

}


const commentUpdate = function(post_pk, comment_pk, updateData) {
  return axios({
    method : 'put',
    url : `http://127.0.0.1:8000/community/post/${post_pk}/comment/${comment_pk}/`,
    headers: {
      'Authorization': `Token ${authStore.token}`
    },
    data : updateData
  })
  .then((response) => {
    
    return response.data;
    
  })
  .catch((error) => {
    console.log(error);
    throw error;
  });

}

const commentDelete = function(post_pk, comment_pk) {
  axios({
    method:'delete',
    url:`http://127.0.0.1:8000/community/post/${post_pk}/comment/${comment_pk}/`,
    headers: {
      'Authorization': `Token ${authStore.token}`
    },
  })
  .then((response) => {
    commentList(post_pk)
    router.push({name:'postdetail', params:{postId:post_pk}})
    
  })
  .catch((error)=>{
    console.log(error)
  })

}
 
 return {postInfos, detailInfos, commentInfos, postList, postDetail, postUpdate, postDelete, commentCreate, commentList, commentUpdate, commentDelete}
}, { persist: true })
