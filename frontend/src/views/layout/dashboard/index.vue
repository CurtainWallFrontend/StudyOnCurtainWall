<!-- 仪表盘页面 -->
<template>
  <div>
    <div class="board">
        <el-row justify="center" style="margin-top: 65px;">
          <el-col :span="8"><el-button style="width:300px;height:180px" @click="GoToSeg" >图像分割</el-button></el-col>
          <el-col :span="8"><el-button style="width:300px;height:180px" @click="GoToExp" >玻璃内爆识别</el-button></el-col>
          <el-col :span="8"><el-button style="width:300px;height:180px" @click="GoToCra" >裂缝和污渍识别</el-button></el-col>
        </el-row>
        <el-row justify="center">
          <el-col :span="8"><el-button style="width:300px;height:180px" @click="GoToVib">风振数据显示</el-button></el-col>
          <el-col :span="8"><el-button style="width:300px;height:180px" @click="GoToMod">3D模型</el-button></el-col>
          <el-col :span="8"></el-col>
        </el-row>
       <!--el-row :gutter="18">
          <el-col :span="15" :offset="1">
            <div class="data-content bg-purple">
              <div style="color:black">风振数据</div>
            </div>
            <div class="button-content bg-purple">
              <el-row>
                <el-col :span="12" style="margin-top: -10px;padding-left: 90px;">
                  <div>
                     <ImgUploader ref="ImgUploadRef" @uploadPicture ="upload" @onCancel="cancel"/>
                  </div>
                  <div class="result-container" v-if="ImgResult">
                      <ImgList :data="ImgResult"/>
                  </div>
                </el-col>
                <el-col :span="12" style="margin-top: 12px;padding-left: 50px;">
                  <el-row><el-button style="width:200px" @click="GoToSeg" >图像分割</el-button></el-row>
                  <el-row><el-button style="width:200px" @click="GoToExp">玻璃内爆识别</el-button></el-row>
                  <el-row><el-button style="width:200px" @click="GoToCra">裂缝和污渍识别</el-button></el-row>
                  <el-row><el-button style="width:200px" @click="GoToVib">风振数据显示</el-button></el-row>
                  <el-row><el-button style="width:200px" @click="GoToMod">3D模型</el-button></el-row>
                </el-col>
              </el-row>
            </div>
          </el-col>
          <el-col :span="7">
            <div class="grid-content bg-purple">
                <div style="color:black">3D模型</div>
            </div>
          </el-col>
        </el-row-->
    </div>
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

.board {
  box-sizing: border-box;
  width: 100%;
  height: 100%;
  padding: 0 30px; /* 给gutter留padding */
}

  .el-row {
    margin-top: 60px;
    margin-bottom: 60px;
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

.el-button--seg.is-active,
.el-button--seg:active {
  background: #20B2AA;
  border-color: #20B2AA;
  color: #fff;
}
 
.el-button--seg:focus,
.el-button--seg:hover {
  background: #AE75E3;
  border-color: #AE75E3;
  color: #fff;
}
 
.el-button--seg {
  color: #FFF;
  background-color: #a85bdb;
  border-color: #a85bdb;
}

.el-button--exp.is-active,
.el-button--exp:active {
  background: #20B2AA;
  border-color: #20B2AA;
  color: #fff;
}
 
.el-button--:focus,
.el-button--exp:hover {
  background: #e37575;
  border-color: #e37575;
  color: #fff;
}
 
.el-button--exp {
  color: #FFF;
  background-color: #db5b5b;
  border-color: #db5b5b;
}

.el-button--cra.is-active,
.el-button--cra:active {
  background: #20B2AA;
  border-color: #20B2AA;
  color: #fff;
}
 
.el-button--:focus,
.el-button--cra:hover {
  background: #e3d275;
  border-color: #e3d275;
  color: #fff;
}
 
.el-button--cra {
  color: #FFF;
  background-color: #dbce5b;
  border-color: #dbce5b;
}

.el-button--vib.is-active,
.el-button--vib:active {
  background: #20B2AA;
  border-color: #20B2AA;
  color: #fff;
}
 
.el-button--:focus,
.el-button--vib:hover {
  background: #759de3;
  border-color: #759de3;
  color: #fff;
}
 
.el-button--vib {
  color: #FFF;
  background-color: #5b84db;
  border-color: #5b84db;
}

.el-button--mod.is-active,
.el-button--mod:active {
  background: #20B2AA;
  border-color: #20B2AA;
  color: #fff;
}
 
.el-button--:focus,
.el-button--mod:hover {
  background: #75e3ae;
  border-color: #75e3ae;
  color: #fff;
}
 
.el-button--mod {
  color: #FFF;
  background-color: #5bdbc1;
  border-color: #5bdbc1;
}

</style>