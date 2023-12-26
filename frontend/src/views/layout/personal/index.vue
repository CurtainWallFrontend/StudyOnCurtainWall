<!-- 个人中心页面 -->
<template>
    <div class="page">
      <h1 class="hello">你好 👋🏻 , user</h1>
      
      <div class="board">
        <div v-if="showChangeForm">
        <!--修改信息界面-->
          <from @submit.prevent="register">
              <el-row><h3 class ="title" style="margin-bottom: 30px;">请输入修改信息</h3></el-row>
              <el-row>
                <el-form-item>
                  <el-input v-model="registerForm.email" 
                  placeholder="邮箱" 
                  required 
                  ref="inputEmail"/>
                </el-form-item>
              </el-row>
              <el-row>
                <el-form-item>
                  <el-input v-model="registerForm.code" 
                  placeholder="验证码" 
                  required>
                    <template #suffix>
                      <button @click.prevent="sendVerificationCode" :disabled="disableButton" style="color: white;background-color: lightgrey;">{{ buttonText }}</button>
                    </template>
                  </el-input>
                </el-form-item>
              </el-row>
              <el-row>
                <el-form-item>
                  <el-input v-model="registerForm.password" 
                  type="password" 
                  placeholder="输入密码" 
                  required 
                  ref="inputPassword"/>
                </el-form-item>
              </el-row>
              <el-row>
                <el-form-item>
                  <el-input v-model="registerForm.confirmPassword" 
                  type="password" 
                  placeholder="确认密码" 
                  required 
                  ref="inputPassword"/>
                </el-form-item>
              </el-row>
              <el-row>
                <el-button class="btn" @click="register">修改</el-button>
                <el-button class="btn" @click="toggleForm">返回</el-button>
              </el-row>
          </from>
        </div>
  
        <div v-else>
        <!--信息展示界面-->
          <el-row>
            <el-col :span="8"><h3 class="title">用户名：user</h3></el-col>
          </el-row>
          <el-row>
            <el-col :span="8"><h3 class="title">邮箱：xxxxx@xx</h3></el-col>
          </el-row>
          <el-row>
            <el-col :span="8"><h3 class="title">其他信息：xxxxxxxx</h3></el-col>
          </el-row>
          <el-row>
            <el-button class="btn" @click="toggleForm">修改信息</el-button>
          </el-row>
        </div>
      </div>
    </div>
  </template>
  
  <script setup>
  import { useUserStore } from '@/api/user';
  import { onMounted,ref } from 'vue'
  
  import axios from 'axios'
  import router from "@/router/index.js"
  import Message from "@/utils/Message.js"
  import ImgUploader from '@/components/ImgUploader.vue'
  import ImgList from '@/components/ImgList.vue'
  import { UploadImg } from '@/api/public.js'
  
  
  const showChangeForm = ref(false);
  const userStore = useUserStore();
  const inputEmail = ref(null);
  const inputPassword = ref(null);
  
  const disableButton = ref(false);
  const buttonText = ref('发送验证码');
  const countdown = ref(60);
  
  
  const registerForm = ref({
    email: '',
    code:'',
    password: '',
  });
  
  //发送验证码
  const sendVerificationCode = async () => {
    if (disableButton.value) {
      return;
    }
    console.log(disableButton.value)
    const success = await userStore.sendVerificationCode(registerForm.email);
  
    if (success) {
      disableButton.value = true;
      startCountdown();
    }
  };
  
  const startCountdown = () => {
    const countdownInterval = setInterval(() => {
      countdown.value--;
  
      if (countdown.value <= 0) {
        clearInterval(countdownInterval);
        resetCountdown();
      } else {
        buttonText.value = `${countdown.value} 秒后重试`;
      }
    }, 1000);
  };
  
  const resetCountdown = () => {
    countdown.value = 60;
    disableButton.value = false;
    buttonText.value = '发送验证码';
  };
  
  // 实现注册逻辑
  const register = () => {
    userStore.register(registerForm.value.email, registerForm.value.code, registerForm.value.password);
    showChangeForm.value = !showChangeForm.value;
  };
  
  const toggleForm = () => {
    showChangeForm.value = !showChangeForm.value;
  };
  
  onMounted(() => {
      userStore.clearUserInfo()
  });
  
  </script>
  
  <style scoped>
  .page{
    background-color: #E8EFF6;
    background-size: cover;
    height: 100%;
    width: 100%;
  }
  .hello {
    position: absolute;
    top:3%;
    left:5%;
    font-size: 14px; 
    color: #8F92A1;
  }
  
  .title {
    font-size: 14px; 
    color: #272835;
  }
  
  .board {
    position: absolute;
    top:10%;
    left:2.2%;
    box-sizing: border-box;
    width: 95%;
  }
  
  .btn{
    margin-top:50px;
    margin-left: 32px;
    width:100px;
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
        color: rgba(183, 183, 183, 0.48); /* 设置分割线颜色为灰色 */
        display: inline-block; /* 将分割线设置为内联块元素*/
        width: 89%; /* 使分割线占满父元素的宽度 */
      }
  
  .el-form-item {
    margin-left: 32px; /* 设置间距大小 */
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
      background-color: white;/*覆盖原背景颜色，设置成透明 */
      border-radius: 5px;
      width:550px;
      height:40px;
      border-color:black;
  }
  
  </style>