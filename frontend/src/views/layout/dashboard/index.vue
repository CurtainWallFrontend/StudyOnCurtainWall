<!-- 仪表盘页面 -->
<template>
  <div class="page">
    <h1 class="hello">你好 👋🏻</h1>
    <h2 class="dashboard">仪表盘</h2>
    <h3 class="func">功能</h3>
    
    <div class="board">
        <el-row justify="center">
          <el-col :span="8"><el-button class="btn" @click="GoToSeg" >图像分割处理</el-button></el-col>
          <el-col :span="8"><el-button class="btn" @click="GoToSmo" >玻璃平整度分析</el-button></el-col>
          <el-col :span="8"><el-button class="btn" @click="GoToCra" >裂缝和污渍识别</el-button></el-col>
        </el-row>
        <el-row justify="center">
          <el-col :span="8"><el-button class="btn" @click="GoToExp" >玻璃自爆识别</el-button></el-col>
          <el-col :span="8"><el-button class="btn" @click="GoToMod">3D模型</el-button></el-col>
          <el-col :span="8"><el-button class="btn" @click="GoToVib">风振数据</el-button></el-col>
          <el-col :span="8"></el-col>
        </el-row>
    </div>
    
    <h3 class="data">数据库</h3>
    <el-column class="database">
          <el-card class="card-item">
            <div class="card-content">
              <span>图像分割 幕墙结果</span>
            </div>
            <div class="card-footer">
              <el-button type="primary" size="small">点击查看</el-button>
            </div>
          </el-card>

          <el-card class="card-item">
            <div class="card-content">
              <span>风振异常数据</span>
            </div>
            <div class="card-footer">
              <el-button type="primary" size="small">点击查看</el-button>
            </div>
          </el-card>

          <el-card class="card-item">
            <div class="card-content">
              <span>玻璃自爆图像</span>
            </div>
            <div class="card-footer">
              <el-button type="primary" size="small">点击查看</el-button>
            </div>
          </el-card>
    </el-column>
      <el-card  class="vib-card">
        <img src="../../../assets/vib.png" class="image">
        <div style="padding: 14px;">
          <div class="bottom clearfix">
            <el-button type="text" class="button" @click="navigateToVibration">点击进入</el-button>
          </div>
        </div>
      </el-card>
  </div>
</template>

<script setup>
import { ref }from 'vue'
import axios from 'axios'
import router from "@/router/index.js"
import Message from "@/utils/Message.js"
import ImgUploader from '@/components/ImgUploader.vue'
import ImgList from '@/components/ImgList.vue'
import { UploadImg } from '@/api/public.js'

const navigateToVibration = () => {
    router.push({ 
        name: 'layout', 
        params:{ 
            choice:'vibration_data' 
        } 
    })
}
const GoToSeg = () => {
    router.push({ 
        name: 'layout', 
        params:{ 
            choice:'segmentation' 
        } 
    })
}
const GoToExp = () => {
    router.push({ 
        name: 'layout', 
        params:{ 
            choice:'explosion_identify' 
        } 
    })
}
const GoToCra = () => {
    router.push({ 
        name: 'layout', 
        params:{ 
            choice:'crack' 
        } 
    })
}
const GoToVib = () => {
    router.push({ 
        name: 'layout', 
        params:{ 
            choice:'vibration' 
        } 
    })
}
const GoToSmo = () => {
    router.push({ 
        name: 'layout', 
        params:{ 
            choice:'smoothness' 
        } 
    })
}
const GoToMod = () => {
    /*router.push({ 
        name: 'layout', 
        params:{ 
            choice:'3Dmodel' 
        } 
    })*/
    window.open('http://120.46.136.85:8888/',"_self");
}

// const fileList = ref();
const ImgUploadRef = ref(null); //上传的图片
const ImgResult = ref(null); //分割后获得的图片
// 这里是一个响应式变量

const GoToDash = () => {
    //跳转仪表盘页面
    router.push({ 
        name: 'layout', 
        params:{ 
            choice:'dashboard' 
        } 
    })
}

const upload = (val) =>{
    console.log(val.fileList[0].raw) //图片raw文件

    let formData = new FormData();
    formData.append('image', val.fileList[0].raw);
    formData.append('func', 'A');

    UploadImg(formData)
        .then(function (result) {  // result 是 api /user/login 的返回值，在后端 api 定义
            // 接收返回值，放在 person_info 变量中
            if(result.status == 200)
                after_upload(result);
        })
        .catch(function (error) {
            console.log(error);
        });
}

const after_upload = (result) => {
    ImgResult.value = result.data;//后期需要修改，先这么写
}
const cancel = () => {
    ImgResult.value = [];
}
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

.dashboard{
  position: absolute;
  top:4%;
  left:5%;
  font-size: 24px; 
}

.func {
  position: absolute;
  top:12%;
  left:2.2%;
  font-size: 14px; 
  color: #272835;
}

.board {
  position: absolute;
  top:16%;
  left:1.5%;
  box-sizing: border-box;
  width: 95%;
}

.btn{
  width:300px;
  height:150px;
  border-radius: 10px;
  border-color: transparent;
}

  .el-row {
    margin-top: 10px;
    margin-bottom: 10px;
    &:last-child {
      margin-bottom: 0;
    }
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
  .grid-content {
    border-radius: 4px;
    min-height: 650px;
  }
  .data-content{
    border-radius: 4px;
    min-height: 352px;
    margin-bottom: 18px;
  }  
  .upload-container{
        position:absolute;
        top:30%;
        left:5%;
    }
  .button-content{
    align-items: center;
    border-radius: 4px;
    min-height: 280px;
  }
  .row-bg {
    padding: 10px 0;
    background-color: #f9fafc;
  }

.data {
  position: absolute;
  top:56%;
  left:2.2%;
  font-size: 14px; 
  color: #272835;
}
.database {
  position: absolute;
  top:62%;
  left:5%;
  display: inline-block;
  vertical-align: top;
}

.card-item {
  text-align: left;
  padding-left: 35px;
  border-radius: 10px;
  width: 400px;

  margin-bottom: 10px;
}

.image-col {
  height: 85%;
  display: flex;
  align-items: stretch;
} 

.vib-card{
  position:absolute;
  top:62%;
  left:45%;
  border-radius: 10px;
  width:585px;
  height:275px;
}
.image {
  width: 100%;
  height: 100%;
}

.card-content{
  font-size: 13px;
}

.card-content,
.card-footer {
  display: flex;
  align-items: center;
}

.card-footer {
  justify-content: flex-end;
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

</style>