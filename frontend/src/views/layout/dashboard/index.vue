<!-- 仪表盘页面 -->
<template>
    <div>
      <div class="board">
          <el-row :gutter="18">
            <el-col :span="15" :offset="1">
              <div class="data-content bg-purple">
                <div style="color:black">风振数据</div>
                <img src="@/assets/vib.png" alt="图片描述" style="width:700px;padding:10px;">
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
                  </el-col>
                </el-row>
              </div>
            </el-col>
            <el-col :span="7">
              <div class="grid-content bg-purple">
                  <div style="color:black">3D模型</div>
              </div>
            </el-col>
          </el-row>
      </div>
    </div>
  </template>
  
  <script setup>
  import { ref, onMounted }from 'vue'
  import axios from 'axios'
  import router from "@/router/index.js"
  import Message from "@/utils/Message.js"
  import ImgUploader from '@/components/ImgUploader.vue'
  import ImgList from '@/components/ImgList.vue'
  import { UploadImg } from '@/api/public.js'
  import { UploadCsv } from '@/api/vibration.js'

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
      router.push({ 
          name: 'layout', 
          params:{ 
              choice:'3Dmodel' 
          } 
      })
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

  const selectedFile = ref()
  const readFileContent = async () => {
    try {
      const response = await axios.get('./assets/example.csv');
      selectedFile.value = response.data;
    } catch (error) {
      console.error(error);
    }
  };

  const showVib = async () => {//展示风振数据图表
        await readFileContent();
        if (selectedFile.value) {
            let formData = new FormData();
            formData.append('csv', selectedFile.value);

            UploadCsv(formData)
                .then(function (result) {
                    chartData.value = result.data;
                    file_url.value = result.data.csv_url;

                    // 绘制echarts折线图
                    var myChart = echarts.init(document.getElementById('main'));
                    let option;
                    let yData=chartData.value.yData;
                    let series = [];
                    for (let name in yData) {
                    series.push({
                        name: name,
                        type: 'line',
                        data: yData[name],
                        smooth: false,
                    })
                    }
                    option = {
                        title: {
                            text: '振动数据风震图'
                        },
                        tooltip: {
                            trigger: 'axis'
                        },
                        legend: {
                            data: ['x', 'y', 'z']
                        },
                        grid: {
                            left: '3%',
                            right: '4%',
                            bottom: '3%',
                            containLabel: true
                        },
                        xAxis: {
                            type: 'category',
                            boundaryGap: false,
                            data: []
                        },
                        yAxis: {
                            type: 'value'
                        },
                        series: series
                    };
                    myChart.setOption(option);

                })
                .catch(function (error) {
                    console.log(error);
                });
        }
        else{
            Message.error('请选择csv文件')
        }
    }
  const cancel = () => {
      ImgResult.value = [];
  }

  onMounted(() => {
  // 在组件挂载后，执行读取文件内容的操作
  readFileContent();
});
  </script>
  
  <style scoped>
  
  .board {
    box-sizing: border-box;
    width: 100%;
    height: 100%;
    padding: 0 30px; /* 给gutter留padding */
  }
  
    .el-row {
      margin-top: 15px;
      margin-bottom: 15px;
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
      height: 815px;
    }
    .data-content{
      border-radius: 4px;
      height: 320px;
    }  
    .upload-container{
          position:absolute;
          top:30%;
          left:5%;
      }
    .button-content{
      align-items: center;
      border-radius: 4px;
      height: 480px;
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