<!-- 登录页面 -->
<template>
    <div class="page">
      <!-- 登录表单 -->
      <div v-if="showLoginForm">
        <form @submit.prevent="login">
          <el-form class="form">
            <h2>欢迎！请登录您的账户</h2>
            <el-form-item>
              <el-input v-model="loginForm.email" 
              placeholder="邮箱" 
              required 
              @keydown.enter="focusNextInput"
              ref="inputEmail"/>
            </el-form-item>

            <el-form-item>
              <el-input v-model="loginForm.password" 
              type="password" 
              placeholder="密码" 
              required 
              @keydown.enter="login"
              ref="inputPassword"/>
            </el-form-item>
            
            <el-form-item>
                <el-button @click="login">登录</el-button>
            </el-form-item>
          </el-form>
        </form>
        <el-form class="register">
          <el-form-item>
            <p @click="toggleForm"
            style="color: rgb(193, 193, 193);
                 cursor: pointer;">没有账户？点击注册</p>
          </el-form-item>
        </el-form>
      </div>
      
      <!-- 注册表单 -->
      <div v-else>
        <form @submit.prevent="register" class="register-form">
          <h2>注册</h2>
          <label for="email">邮箱:</label>
          <el-input v-model="registerForm.email" required />
          <div class="verification-code">
            <label for="verificationCode">验证码:</label>
            <el-input v-model="registerForm.code" required />
            <button @click.prevent="sendVerificationCode" :disabled="disableButton" style="color: white;">
              {{ buttonText }}
            </button>
          </div>
          <div>
            <label for="password">输入密码:</label>
            <el-input v-model="registerForm.password" type="password" required />
          </div>
          <div>
            <label for="confirmPassword">确认密码:</label>
            <el-input v-model="registerForm.confirmPassword" type="password" required />
          </div>
          <button type="submit" style="color: white;">注册</button>
          <p @click="toggleForm" 
          style="color: rgb(193, 193, 193);
                 cursor: pointer;">已有账户？点击登录</p>
        </form>
    </div>
  <el-button @click="GoToLayout">点击跳转排版页面</el-button>
</div>

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
const inputEmail = ref(null);
const inputPassword = ref(null);

const loginForm = ref({
  email: '',
  password: '',
});

const registerForm = ref({
  email: '',
  code:'',
  password: '',
});

const focusNextInput = () => {
  inputPassword.value.focus();
}

const login = async () => {
  const loginSuccess = await userStore.login(loginForm.value.email, loginForm.value.password);
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
  userStore.register(registerForm.value.email, registerForm.value.code, registerForm.value.password);
};

const logout = () => {
  // 实现退出登录逻辑
  userStore.clearUserInfo();
};

const toggleForm = () => {
  showLoginForm.value = !showLoginForm.value;
};

onMounted(() => {
    userStore.clearUserInfo()
});


</script>

<style scoped>
.page{
  background-image: url('@/assets/background.png');
  background-size: cover;
  position: fixed;
  top: 0;
  left: 0;
  height: 100vh;
  width: 100vw;
}
.form{
  position: absolute;
  color: white;
  top: 35%;
  left: 70%;
  display: flex;
  flex-direction: column;
  align-items: center;
}

.el-form-item + .el-form-item {
  margin-top: 20px; /* 设置间距大小 */
}

.button{
  position: absolute;
    top: 64%;
    left: 79%;
    height: 10%;
    width: 14%;
}
.register{
  position: absolute;
    top: 62%;
    left: 74%;
    height: 10%;
    width: 20%;
}

.el-input {
  height: 28px; 
  width: 250px;
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

.el-button{
  height: 37px;
  width: 198px;
  background-color: rgb(4, 4, 80);
  color: white;
  border-color: transparent;
}

.register-form{
  position:absolute;
  top:39%;
  left:80%;
}
</style>