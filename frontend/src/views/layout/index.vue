<!-- 排版页面 -->
<template>
    <div>
        <!-- 侧边栏区域begin -->
        <div :class="[{ 'menu': showSideBar }, { 'menu-none': !showSideBar }]">
            <el-icon @click="showSideBar = true" v-show="!showSideBar" class="showMenu"><Expand /></el-icon>
            <el-icon @click="showSideBar = false" v-show="showSideBar" class="hideMenu"><Fold /></el-icon>
            <SideBar class="SideBar" v-show="showSideBar" />
        </div>
        <!-- 侧边栏区域end -->
    </div>

    <!-- 右侧功能区域begin -->
    <div :class="[{ 'func-zone': showSideBar }, { 'func-zone-center': !showSideBar }]">
        <dashboard v-if="choice == 'dashboard'" />
        <segmentation v-if="choice == 'segmentation'" />
        <smoothness v-if="choice == 'smoothness'" />
        <crack v-if="choice == 'crack'" />
        <explosion_identify v-if="choice == 'explosion_identify'" />
        <vibration v-if="choice == 'vibration'" />
        <vibrationData v-if="choice == 'vibration_data'" />
        <model v-if="choice == 'model'" />
        <personal v-if="choice == 'personal'" />
        <auth v-if="choice == 'auth_mgmt'" />
    </div>
</template>

<script setup>
import { ref, reactive, onMounted, onUpdated, computed } from 'vue'
import SideBar from '@/components/SideBar.vue'
import dashboard from '@/views/layout/dashboard/index.vue'
import smoothness from '@/views/layout/smoothness/index.vue'
import crack from '@/views/layout/crack/index.vue'
import segmentation from '@/views/layout/segmentation/index.vue'
import explosion_identify from '@/views/layout/explosion_identify/index.vue'
import vibration from '@/views/layout/vibration/index.vue'
import vibrationData from '@/views/layout//vibration_data/index.vue'
import model from '@/views/layout/3Dmodel/index.vue'
import personal from '@/views/layout/personal/index.vue'
import auth from '@/views/layout/auth_mgmt/index.vue'
import { useRoute } from 'vue-router'
import { Expand } from '@element-plus/icons-vue'
import { Fold } from '@element-plus/icons-vue'

const route = useRoute();
const choice = ref();//根据路由传值对应功能区的显示内容

const showSideBar = ref(false);

// 监听路由变化并执行不同逻辑
onMounted(() => {
    updateLogic();
});
onUpdated(() => {
    updateLogic();
});

// 执行不同逻辑的函数
const updateLogic = () => {
    switch (route.params.choice) {
        case 'dashboard':
            choice.value = 'dashboard'
            break;
        case 'segmentation':
            choice.value = 'segmentation'
            break;
        case 'smoothness':
            choice.value = 'smoothness'
            break;
        case 'crack':
            choice.value = 'crack'
            break;
        case 'explosion_identify':
            choice.value = 'explosion_identify'
            break;
        case 'vibration':
            choice.value = 'vibration'
            break;
        case 'vibration_data':
            choice.value = 'vibration_data'
            break;
        case 'model':
            choice.value = 'model'
            break;
        case 'personal':
            choice.value = 'personal'
            break;
        case 'auth_mgmt':
            choice.value = 'auth_mgmt'
            break;
    }
}
</script>

<style scoped>
.menu {
    position: fixed;
    left: 0%;
    top: 0%;
    width: 18%;
    height: 100%;
    background-color: #00205B;
    color: white;
}

.menu-none {
    position: fixed;
    left: 0%;
    top: 0%;
    width: 3%;
    height: 100%;
    z-index: 99;
    background-color: #E8EFF6;
}

.func-zone {
    position: absolute;
    left: 18%;
    top: 0%;
    width: 82%;
    height: 100%;
    background-color: #E8EFF6;
}

.func-zone-center {
    position: absolute;
    left: 0%;
    top: 0%;
    width: 100%;
    height: 100%;
    background-color: #E8EFF6;
}

.showMenu {
    color:#00205B;
    font-size: 24px; /* 改变图标大小 */
    left: 10px;
    top: 25px;
}

.showMenu:hover {
    font-size: 24px; /* 改变图标大小 */
    left: 10px;
    top: 25px;
    opacity: 0.7;
}

.hideMenu {
    font-size: 24px; /* 改变图标大小 */
    left: 92px;
    top: 25px;
}

.hideMenu:hover {
    font-size: 24px; /* 改变图标大小 */
    left: 92px;
    top: 25px;
    opacity: 0.8;
}
</style>