<template>
    <div>这是振动数据风震图页面</div>
    <el-button @click="GoToDash">进入仪表盘</el-button>

    <div>
        <h2>1.请上传振动数据文件（csv）</h2>
        <input type="file" ref="fileInput"  accept=".csv" @change="handleFileInputChange" />
        <button @click="uploadFile" :disabled="!selectedFile">上传文件</button>
    </div>

    <h2 v-if="selectedFile" style="margin:30px">2.请选择异常阈值</h2>
    <div v-if="selectedFile" class="slider-block" style="width: 400px;">
        <el-slider v-model="range" range step="0.1" :min="-5" :max="5"  range-start-label range-end-label/>
        <div>异常值上下限：【{{ range[0] }}，{{ range[1] }}】</div>
    </div>

    <h2 v-if="selectedFile" style="margin:30px">3.异常值筛选</h2>
    <div v-if="selectedFile" id="abnormal" style="width: 100%;height:500px;">
    </div>


    <h2 v-if="selectedFile" style="margin:30px">4.风震图显示</h2>
    <div v-if="selectedFile" id="main" style="width: 100%;height:500px;">
    </div>
</template>

<script setup>
    import router from "@/router/index.js"
    import { UploadCsv } from '@/api/vibration.js'
    import { ref, reactive } from 'vue'
    import * as echarts from 'echarts';

    // const chartData = reactive({
    //     yData: {
    //       'x': [-0.02632,-0.09632,-0.05632,0.03368,0.04368,0.12368,0.09368,-0.22632,-0.02632,-0.00632,-0.09632,
    //       0.03368,-0.00632,0.00368,0.03368,-0.09632,-0.08632,-0.08632,-0.07632,-0.05632],
    //       'y': [0.074566,0.084576,0.124554,-0.065449,-0.105427,-0.065449,-0.055439,-0.075458,-0.085468,-0.035419,
    //       0.084576,0.024578,0.104534,0.104534,-0.045429,0.014568,0.034588,0.044537,0.014568,-0.035419],
    //       'z': [0.11136,0.21136,0.05136,-0.04864,-0.27864,0.04136,0.14136,0.13136,-0.05864,-0.13864,-0.03864,
    //       0.02136,-0.08864,0.25136,0.25136,0.04136,0.01136,0.02136,0.03136,0.02136]
    //     }
    //   });

    var chartData = ref();

    const range = ref([-0.5, 0.5])

    const fileInputRef = ref(null);
    const selectedFile = ref(null); //已选文件

    const GoToDash = () => {
        //跳转仪表盘页面
        router.push({ 
            name: 'layout', 
            params:{ 
                choice:'dashboard' 
            } 
        })
    }


    const handleFileInputChange = (event) => {
        const file = event.target.files[0];
        selectedFile.value = file;
        console.log(selectedFile.value);
        console.log(typeof range[0]);
    };


    const uploadFile = () => {
    if (selectedFile.value) {
        let formData = new FormData();
        formData.append('csv', selectedFile.value);

        formData.append('min', range.value[0]); //最低阈值 
        formData.append('max', range.value[1]); //最高阈值
        UploadCsv(formData)
            .then(function (result) {
                chartData.value = result.data;

                var myChart = echarts.init(document.getElementById('main'));
                var myAbnormalChart = echarts.init(document.getElementById('abnormal'));

                let option;
                let optionAbnormal;

                let yData = chartData.value.yData;
                let yDataAbnormal = chartData.value.abnormal;

                let series = [];
                let seriesAbnormal = [];

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
                                        return '异常上限';
                                    } else if (params.name === 'Min') {
                                        return '异常下限';
                                    }
                                },
                                color: '#ff0000'
                            }
                        }
                    })
                }

                for (let name in yDataAbnormal) {
                    seriesAbnormal.push({
                        name: name,
                        type: 'line',
                        data: yDataAbnormal[name],
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
                                        return '异常上限';
                                    } else if (params.name === 'Min') {
                                        return '异常下限';
                                    }
                                },
                                color: '#ff0000'
                            }
                        }
                    })
                }


                option = {
                    title: {
                        text: 'Curtain Vib'
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
                    },
                    series: series,
                };

                optionAbnormal = {
                    title: {
                        text: 'Curtain Abnormal Vib'
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
                        // min: range.value[0], // 设置 yAxis 的最小值为最低阈值和数据中的最小值中的较小者
                        // max: range.value[1] // 设置 yAxis 的最大值为最高阈值和数据中的最大值中的较大者
                    },
                    series: seriesAbnormal,
                };



                myChart.setOption(option);
                myAbnormalChart.setOption(optionAbnormal);
            })
            .catch(function (error) {
                console.log(error);
            });
    }
};

</script>

<style>

    .upload-container{
        margin:30px;
    }

    .slider-block{
        margin: auto;
    }

</style>