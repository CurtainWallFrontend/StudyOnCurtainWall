<!-- 个人中心页面 -->
<template>
  <div class="page">
    <h1 class="hello">你好 👋🏻</h1>
    <h2 class="person">个人中心</h2>

    <div class="board">
      <el-row>
        <el-col :span="3">
          <el-row class="upload-container" style="margin-top:45px;">
            <el-upload ref="uploadRef" :class="uploadClass" action="''" list-type="picture-card" :auto-upload="false"
              :on-remove="handleRemove" :on-preview="handlePreview" :on-change="handleChange"
              :show-file-list="isSelectedShow">
              <el-icon>
                <Plus />
              </el-icon>
            </el-upload>
            <el-dialog v-model="dialogVisible" height="705px">
              <div class="picture-container">
                <img w-full :src="dialogImageUrl" alt="Preview Image" class="picture" />
              </div>
            </el-dialog>
            <el-button type="primary" class="btn">退出登录</el-button>
          </el-row>

        </el-col>
        <el-col :span="9">
          <el-row style="margin-top: 60px;margin-left: 20px;">
            <h3 class="personName">{{ personInfo.name }}</h3>
          </el-row>
          <el-row style="margin-top: 90px;margin-left: 20px;">
            <el-col :span="13">
              <h3 class="info">Email : {{ personInfo.email }}</h3>
            </el-col>
            <el-col :span="10"><el-button>更换邮箱</el-button></el-col>
          </el-row>
        </el-col>
        <el-col :span="12">
          <el-row style="margin-top: 60px;">
            <h3 class="info">电话 : {{ personInfo.phone }}</h3>
          </el-row>
          <el-row style="margin-top: 45px;">
            <h3 class="info">单位 : {{ personInfo.company }}</h3>
          </el-row>
          <el-row style="margin-top: 45px;">
            <h3 class="info">其他信息 : {{ personInfo.other }}</h3>
          </el-row>
        </el-col>
      </el-row>

      <el-row style="margin-top: 45px;">
        <h3 class="notice">系统通知</h3>
      </el-row>
      <el-row style="margin-top: 45px;">
        <h3 class="info">xxxxxxxxxxxxxxxxxxx</h3>
      </el-row>
    </div>
  </div>
</template>

<script setup>
import { computed, reactive } from 'vue'
import { ElMessage, ElUpload, ElIcon, ElButton, ElDialog, ElRow } from 'element-plus'
import { Plus } from '@element-plus/icons-vue'
import { useUserStore } from '@/api/user';
import { onMounted, ref } from 'vue'

import router from "@/router/index.js"
import Message from "@/utils/Message.js"
import ImgUploader from '@/components/ImgUploader.vue'
import ImgList from '@/components/ImgList.vue'
import { UploadImg } from '@/api/public.js'

const userStore = useUserStore();

const personInfo = ref({
  name: '',
  email: '',
  phone: '1919810',
  company: '同济大学',
  other: 'xxxxxxxx',
});

const user = JSON.parse(localStorage.getItem('user')).userInfo.token;

const getInfo = async () => {
  const result = await userStore.getCurrentInfo(user);

  personInfo.value.name = result.username;
  personInfo.value.email = result.email;
}
getInfo();

const handleRemove = () => {

}
const handlePreview = () => {
  
}
const handleChange = () => {
  
}

onMounted(() => {
  userStore.clearUserInfo()
});

</script>

<style scoped>
.page {
  background-color: #E8EFF6;
  background-size: cover;
  height: 100%;
  width: 100%;
}

.hello {
  position: absolute;
  top: 3%;
  left: 5%;
  font-size: 14px;
  color: #8F92A1;
}

.info {
  position: absolute;
  font-size: 14px;
  color: #8F92A1;
}

.person {
  position: absolute;
  top: 4%;
  left: 5%;
  font-size: 24px;
  color: #272835;
}

.title {
  font-size: 14px;
  color: #272835;
}

.personName {
  position: absolute;
  font-size: 18px;
  color: #272835;
}

.notice {
  position: absolute;
  font-size: 14px;
  color: #272835;
}

.board {
  position: absolute;
  top: 10%;
  left: 2.2%;
  box-sizing: border-box;
  width: 95%;
}

.btn {
  margin-top: 20px;
  margin-left: 30px;
  border-color: transparent;
}

.el-row {
  margin-top: 10px;
  margin-bottom: 10px;

}

.el-col {
  border-radius: 4px;
}

.bg-purple-dark {
  background: #99a9bf;
}

.bg-purple {
  background: #d3dce6;
}

.bg-purple-light {
  background: #e5e9f2;
}

.row-bg {
  padding: 10px 0;
  background-color: #f9fafc;
}

h3 {
  font-size: 16px;
  text-align: left;
  margin-top: 5px;
  padding-left: 35px;
}

hr {
  margin-left: 10px;
  color: rgba(183, 183, 183, 0.48);
  /* 设置分割线颜色为灰色 */
  display: inline-block;
  /* 将分割线设置为内联块元素*/
  width: 89%;
  /* 使分割线占满父元素的宽度 */
}

.el-form-item {
  margin-left: 32px;
  /* 设置间距大小 */
  margin-bottom: 20px;
}

.el-input {
  height: 30px;
  width: 280px;
}

/*搜索组件最外层div */
.input_box {
  margin-right: 15px;
}

/*搜索input框 */
:deep(.el-input__wrapper) {
  background-color: white;
  /*覆盖原背景颜色，设置成透明 */
  border-radius: 5px;
  width: 550px;
  height: 40px;
  border-color: black;
}
</style>