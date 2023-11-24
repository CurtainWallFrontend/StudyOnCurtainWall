<template>
    <div>这是振动数据风震图页面</div>
    <el-button @click="GoToDash">进入仪表盘</el-button>

    <div>
        <h2>1.请上传振动数据文件（csv）</h2>
        <!-- <div style="width: 50%; margin:auto;text-align: center;">
            <el-form label-width="auto" ref="formRef" :model="selectedInfo" :rules="fileRules">
                <el-form-item label="采集时间" prop="time">
                <el-date-picker
                    v-model="selectedInfo.time"
                    type="datetimerange"
                    range-separator="至"
                    start-placeholder="开始时间"
                    end-placeholder="结束时间"
                />
                </el-form-item>
                <el-form-item label="选择设备" prop="equipment">
                    <el-cascader v-model="selectedInfo.equipment" 
                        :options="options" 
                        placeholder="请选择建筑/传感器编号" 
                        @change="change_select" 
                        clearable/>
                </el-form-item>
            </el-form>
        </div> -->
        <input type="file" ref="fileInput"  accept=".csv" @change="handleFileInputChange" />
        <button @click="uploadFile" :disabled="!selectedFile">上传文件</button>
    </div>


    <h2 v-if="showNormal" style="margin:30px">2.风震图显示</h2>
    <div id="main" style="width: 100%;height:500px;"></div>

    <h2 v-if="showNormal" style="margin:30px">3.请选择异常阈值</h2>
    <div v-if="showNormal" class="slider-block" style="width: 400px;">
        <el-slider v-model="range" range step="0.1" :min="-5" :max="5"  range-start-label range-end-label/>
        <div>异常值上下限：【{{ range[0] }}，{{ range[1] }}】</div>
        <div style="margin:20px">
            <el-button @click="filterOutlier">确认筛选</el-button>
        </div>
    </div>

    <h2 v-if="showAbnormal" style="margin:30px">4.异常值筛选结果</h2>
    <div id="abnormal" style="width: 100%;height:500px;"></div>
</template>

<script setup>
    import router from "@/router/index.js"
    import { UploadCsv, FilterOutlier } from '@/api/vibration.js'
    import { ref, reactive } from 'vue'
    import * as echarts from 'echarts';
    import { ElMessage } from "element-plus";

    var chartData = ref();
    var abnormalChartData = ref();

    const range = ref([-0.5, 0.5])

    const selectedFile = ref(null); //已选文件
    const file_url = ref('');//文件url

    const showNormal = ref(false);//显示平滑后的风震图
    const showAbnormal = ref(false); //显示异常风震图

    // 暂时写死：后期存储到数据库中，可以由用户自行添加建筑、设备型号；
    // 从后端获取这些数据或选择
    const options = ref([
        {
            'value': 'A楼',
            'label': 'A楼',
            'children':[
                {
                   'value': 'A77C5238',
                    'label': 'A77C5238',
                },
                {
                    'value': 'F853ED49',
                    'label': 'F853ED49',
                },
                {
                    'value': '3326F78D',
                    'label': '3326F78D',
                },
                {
                    'value': '350E6EFF',
                    'label': '350E6EFF',
                },
            ]
        },
        {
            'value': '综合楼',
            'label': '综合楼',
            'children':[
                {
                    'value': 'E884C99D',
                    'label': 'E884C99D',
                },
                {
                    'value': '7749E4D9',
                    'label': '7749E4D9',
                },
                {
                    'value': '7A6BA8C8',
                    'label': '7A6BA8C8',
                },
                {
                    'value': '8850A7D7',
                    'label': '8850A7D7',
                },
                {
                    'value': '4787BE3A',
                    'label': '4787BE3A',
                },
            ]
        },
        {
            'value': '经管大楼',
            'label': '经管大楼',
            'children':[
                {
                    'value': '29FA1867',
                    'label': '29FA1867',
                },
                {
                    'value': '350E6EFF',
                    'label': '350E6EFF',
                },
                {
                    'value': '3326F78D',
                    'label': '3326F78D',
                },
                {
                    'value': 'A77C5238',
                    'label': 'A77C5238',
                },
                {
                    'value': 'E43AC643',
                    'label': 'E43AC643',
                },
                {
                    'value': '4787BE3A',
                    'label': '4787BE3A',
                },
            ]
        },
    ]);

    // 已选传感器信息
    // const selectedInfo = ref({
    //     'equipment': [],
    //     //数组：equipment[0]代表建筑，equipment[1]代表传感器编号
    //     'time': [],
    //     //时间数组：time[0]开始时间，time[1]是结束时间
    // })

    // const change_select = () =>{
    //     console.log(selectedInfo.value.equipment)
    //     // console.log(selectedInfo.value.equipment[0])
    // }

    // const validateTime = (rule, value, callback) => {
    //     if(!value){
    //         callback(new Error('请选择时间'))
    //     }
    //     else{
    //         console.log(value);
    //         callback();
    //     }
    // }

    // const validateEquipment = (rule, value, callback) => {
    //     if(!value){
    //         callback(new Error('请选择建筑/传感器编号'))
    //     }
    //     else{
    //         callback();
    //     }
    // }

    // // 表单规则
    // const fileRules = ref({
    //     time:[{
    //         validator:validateTime,
    //         trigger:'change',
    //     }],
    //     equipment:[{
    //         validator:validateEquipment,
    //         trigger:'change',
    //     }]
    // })

    // const formRef = ref(null);


    // 跳转到仪表盘
    const GoToDash = () => {
        //跳转仪表盘页面
        router.push({ 
            name: 'layout', 
            params:{ 
                choice:'dashboard' 
            } 
        })
    }


    // 选择文件
    const handleFileInputChange = (event) => {
        const file = event.target.files[0];
        selectedFile.value = file;
        console.log(selectedFile.value);
    };

    // 上传文件
    const uploadFile = () => {
        // formRef.value.validate((valid) => {
            // if(valid){   //表单验证成功
                if (selectedFile.value) {
                    let formData = new FormData();
                    formData.append('csv', selectedFile.value);
                    // formData.append('building', selectedInfo.value.equipment[0])
                    // formData.append('equipment', selectedInfo.value.equipment[1])
                    // formData.append('start_time', selectedInfo.value.time[0])
                    // formData.append('end_time', selectedInfo.value.time[1])

                    // formData.append('min', range.value[0]); //最低阈值 
                    // formData.append('max', range.value[1]); //最高阈值

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

                            showNormal.value = true;
                        })
                        .catch(function (error) {
                            console.log(error);
                        });
                }
            //     else{
            //         ElMessage.error('请选择csv文件')
            //     }
            // }
            else{
                ElMessage.error('请检查表单是否填写正确！')
            }
        // })

    };


    // 异常值筛选
    const filterOutlier = () => {
        // 向后端发送请求
        let formData = new FormData();
        formData.append('min',range.value[0])
        formData.append('max',range.value[1])
        formData.append('csv_url',file_url.value)
        console.log(file_url.value)

        FilterOutlier(formData)
        .then(function(result){

            // 绘制echarts折线图
            var myChart = echarts.init(document.getElementById('abnormal'));
            let option;
            let yData=result.data.yData;
            let series = [];
            for (let name in yData) {
                series.push({
                    name: name,
                    type: 'line',
                    data: yData[name],
                    smooth: false,
                    markLine: {
                                data: [
                                    { type: 'none', name: 'Max', yAxis: range.value[1] },
                                    { type: 'none', name: 'Min', yAxis: range.value[0] }
                                ],
                                itemStyle: {
                                    normal: {
                                        lineStyle: {
                                            color: '#ff0000',
                                        }
                                    }
                                },
                                label: {
                                    position: 'end',
                                    formatter: function (params) {
                                        if (params.name === 'Max') {
                                            return '异常上限{{range.value[1]}}';
                                        } else if (params.name === 'Min') {
                                            return '异常下限{{range.value[0]}}';
                                        }
                                    },
                                    color: '#ff0000'
                                }
                            }
                })
            }



            option = {
                title: {
                    text: '异常值风震图'
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
                    type: 'value',
                    min: Math.min(range.value[0], Math.min(...yData['x']), Math.min(...yData['y']), Math.min(...yData['z']),),
                    max: Math.max(range.value[1], Math.max(...yData['x']), Math.max(...yData['y']),Math.max(...yData['z'])),
                },
                series: series
            };
            myChart.setOption(option);

            showAbnormal.value = true;
        })
        .catch(function (error) {
            console.log(error);
        });
    }
    

</script>

<style>

    .upload-container{
        margin:30px;
    }

    .slider-block{
        margin: auto;

    }

</style>