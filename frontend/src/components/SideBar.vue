<!-- 侧边栏页面 -->
<template>
    <el-aside width=100%>
        <h2>LOGO</h2>
        <el-menu :default-active="defaultActive" router class = "menu" @select="handleSelect">
            <el-menu-item index="dashboard" style="color:rgb(226, 226, 226);">
              仪表盘
            </el-menu-item>
            <el-sub-menu index="dashboard">
                <template #title>
                    <span style="color:rgb(204, 204, 204);">功能</span>
                </template>
                <a href = "http://43.142.78.122:5173/"><el-menu-item>图像分割处理</el-menu-item></a>
                <el-menu-item index="smoothness">玻璃平整度分析</el-menu-item>
                <!-- 王诗腾 -->
                <el-menu-item index="crack">裂缝和污渍识别</el-menu-item>
                <a href = "http://47.117.145.92/"><el-menu-item index="explosion_identify">玻璃内爆识别</el-menu-item></a>
                <el-menu-item index="vibration">异常风振数据</el-menu-item>
                <a href = "http://120.46.136.85:8888/"><el-menu-item>3D模型</el-menu-item></a>
            </el-sub-menu>
            <el-sub-menu index="database">
                <template #title>
                    <span style="color:rgb(204, 204, 204);">数据库</span>
                </template>
                <el-menu-item index="vibration_data">风振数据</el-menu-item>
            </el-sub-menu>
            <el-menu-item index="personal" style="color:rgb(226, 226, 226);">
                个人中心
            </el-menu-item>
        </el-menu>
    </el-aside>
</template>
  

<script setup>
import { useUserStore } from '@/api/user';
import router from "@/router/index.js"
import { ref, onMounted } from 'vue'
import { useRouter, useRoute } from "vue-router";

const defaultActive = ref('dashboard')
const userStore = useUserStore();
const userEmail = ref();

const get_Email = async () => {
  var popup = window.open("http://47.117.145.92/");
  if (popup) {
    const user = {
      'email':userEmail,
    }
    const success = await userStore.sendVerificationCode(registerForm.value.email);
    setTimeout(function () {
      var data = {
        email: userEmail
      };
      popup.postMessage(JSON.stringify(data), "http://47.117.145.92/");
    }, 500);
  }
}

const handleSelect = (index) => {
  localStorage.setItem('lastActiveMenuItem', index);
};

onMounted(() => {
  defaultActive.value = localStorage.getItem('lastActiveMenuItem') ?? '';
});


</script>

<style scoped>
.menu {
  position: absolute;
  top: 10%;
  left: 0%;
  width: 100%;
  background-color: #2a3f75;
}

.el-sub-menu .el-menu-item {
  background-color: #506baf !important;
  color: rgb(204, 204, 204);
}

/* 设置选鼠标指针浮动在一级菜单的设置 */
.el-menu-item:hover {
  background-color: rgb(235, 235, 235) !important;
  ;
}

/* 设置当前被选中的一级菜单 */
.el-menu-item.is-active {
  color: white !important;
  background: black !important;
}
</style>