<template>
  <div class="page">
    <h1 class="hello">你好 👋🏻</h1>
    <h2 class="auth">用户权限管理</h2>

    <!-- 搜索栏 -->
    <div class="search-container">
      <div class="search">
        <el-input placeholder="请输入用户关键词" v-model="formData.keyword" @keyup.enter="enterDown">
          <template #append>
            <el-button @click="enterDown">
              <el-icon>
                <Search />
              </el-icon>
            </el-button>
          </template>
        </el-input>
      </div>
    </div>
    <div class="table_container">
      <table class="user_table">
        <thead class="table_header">
          <tr>
            <th>ID</th>
            <th>Name</th>
            <th>Email</th>
            <th>是否为管理员</th>
            <th>3D模型权限</th>
            <th>污渍裂缝识别权限</th>
            <th>玻璃自爆权限</th>
            <th>玻璃幕墙分割权限</th>
            <th>异常风振数据权限</th>
          </tr>
        </thead>
        <tbody class="table_body">
          <tr v-for="(item, index) in itemList" :key="item.id">
            <td>{{ item.id }}</td>
            <td>{{ item.username }}</td>
            <td>{{ item.email }}</td>
            <!-- <td>{{ item.is_superuser }}</td> -->
            <td>
              <el-switch v-model="item.is_superuser" @change="handleSwitchChange(item, index, 'is_superuser')" />
            </td>
            <td>
              <el-switch v-model="item.access_system_a" @change="handleSwitchChange(item, index, 'access_system_a')" />
            </td>
            <td>
              <el-switch v-model="item.access_system_b" @change="handleSwitchChange(item, index, 'access_system_b')" />
            </td>
            <td>
              <el-switch v-model="item.access_system_c" @change="handleSwitchChange(item, index, 'access_system_c')" />
            </td>
            <td>
              <el-switch v-model="item.access_system_d" @change="handleSwitchChange(item, index, 'access_system_d')" />
            </td>
            <td>
              <el-switch v-model="item.access_system_e" @change="handleSwitchChange(item, index, 'access_system_e')" />
            </td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted, nextTick } from "vue";
import { GetAuth } from "@/api/public.js";

const selected_item = ref("1");

const handleSelect = (key, keyPath) => {
  console.log(key, keyPath);
};

const itemList = ref([]);

const handleSwitchChange = (item, index, key) => {
  console.log(item.is_superuser)
  //完成POST到后端的逻辑
}

const formData = reactive({  // 用 reactive，而不用 ref
  keyword: '',
});

onMounted(() => {
  // 绑定监听事件
  nextTick(() => {
    window.addEventListener("keydown", enterDown);
  });
});

const enterDown = async () => {
  if (!formData.keyword) {
    Message.error("请输入用户关键词！");
    return;
  }
  //进行搜索操作

}

//发送请求
GetAuth()
  .then(function (result) {
    itemList.value = result.data.users;
    console.log(itemList.value);
  })
  .catch(function (error) {
    console.log(error);
  })
  .finally(() => {
    // loading.value = false;
  });
</script>

<style scoped>
.el-menu {
  background: linear-gradient(270deg,
      rgba(172, 176, 255, 0.94) 3.68%,
      rgba(209, 241, 255, 0.97) 34.53%,
      rgba(210, 241, 255, 0.97) 34.54%,
      rgba(251, 254, 255, 0.98) 58.26%,
      rgba(254, 254, 255, 1) 94.07%,
      #d8e6ff 99.65%,
      #fefeff 99.87%);
  height: 7vh;
}

.router-link-active {
  text-decoration: none;
  color: #409eff;
}

a {
  text-decoration: none;
  color: black;
}

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

.auth {
  position: absolute;
  top: 4%;
  left: 5%;
  font-size: 24px;
  color: #272835;
}

.table_container {
  display: flex;
  justify-content: center;
}

.table_header {
  height: 60px;
  background-color: rgb(215, 233, 255)
}

.table_body {
  vertical-align: top;
}

.user_table {
  border: 2px solid black;
  color: black;
  position: absolute;
  top: 20%;
  width: 90%;
  height: 600px;
}

.search-container {
  display: flex;
  justify-content: center;
}

.search {
  position: absolute;
  top: 12.5%;
  display: inline-block;
  width:60%;
}

/*搜索组件最外层div */
.input_box {
  margin-right: 15px;
  border-radius: 50%;
}

/*搜索input框 */
:deep(.el-input__wrapper) {
  background-color: white;
  /*覆盖原背景颜色，设置成透明 */
  border-radius: 95px;
  height: 40px;
  border-color: black;
}

/*搜索button按钮 */
:deep(.el-input-group__append) {
  background: #2a3f75;
  border-radius: 50%;
  border: 0;
  color: white;
}
</style>
