<!-- 登录页面 -->
<template>
    <div>本页面为登录/注册页面</div>
    <div class="login-register">
    <div v-if="!userStore.isAuthenticated">
      <!-- 登录表单 -->
      <div v-if="showLoginForm">
        <h2>登录</h2>
        <form @submit.prevent="login">
          <label for="email">邮箱:</label>
          <input v-model="loginForm.email" type="text" required />
          <label for="password">密码:</label>
          <input v-model="loginForm.password" type="password" required />
          <button type="submit" style="color: white;">登录</button>
        </form>
        <p @click="toggleForm">没有账户？点击注册</p>
      </div>
      <!-- 注册表单 -->
      <div v-else>
        <h2>注册</h2>
        <form @submit.prevent="register">
          <label for="email">邮箱:</label>
          <input v-model="registerForm.email" type="text" required />
          <div class="verification-code">
            <label for="verificationCode">验证码:</label>
            <input v-model="registerForm.code" type="text" required />
            <button @click.prevent="sendVerificationCode" :disabled="disableButton" style="color: white;">
              {{ buttonText }}
            </button>
          </div>
          <div>
            <label for="password">输入密码:</label>
            <input v-model="registerForm.password" type="password" required />
          </div>
          <div>
          <label for="confirmPassword">确认密码:</label>
          <input v-model="registerForm.confirmPassword" type="password" required />
          </div>
          <button type="submit" style="color: white;">注册</button>
        </form>
        <p @click="toggleForm">已有账户？点击登录</p>
      </div>
    </div>
    <div v-else>
      <p>欢迎，{{ userStore.userInfo.email }}！</p>
      <button @click="logout">退出登录</button>
    </div>
  </div>



  <el-button @click="GoToLayout">点击跳转排版页面</el-button>


</template>

<script setup>
import { useUserStore } from '@/api/user';
import { onMounted,ref } from 'vue'
import router from "@/router/index.js"

const GoToLayout = () => {
    router.push({ 
        name: 'layout', 
        params:{ 
            choice:'dashboard' 
        } 
    })
}

const showLoginForm = ref(true);
const userStore = useUserStore();

const loginForm = {
  email: '',
  password: '',
};

const registerForm = {
  email: '',
  code:'',
  password: '',
};

const login = async () => {
  const loginSuccess = await userStore.login(loginForm.email, loginForm.password);
  if (loginSuccess) {
    router.push({  name: 'layout', params: { choice: 'dashboard'}});
  } else {
    console.error(error.message);
  }
};


const disableButton = ref(false);
const buttonText = ref('发送验证码');
const countdown = ref(60);

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


const register = () => {
  // 实现注册逻辑
  userStore.register(registerForm.email, registerForm.code, registerForm.password);
};

const logout = () => {
  // 实现退出登录逻辑
  userStore.logout();
};

const toggleForm = () => {
  showLoginForm.value = !showLoginForm.value;
};







onMounted(() => {
    userStore.clearUserInfo()
});


</script>

<style scoped>

</style>