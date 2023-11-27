<template>
    <div>这是振动数据风震图页面</div>
    <el-button @click="GoToDash">进入仪表盘</el-button>

    <div style="width: 50%; margin: 30px auto;text-align: center;">
        <h3>选择条件进行数据查找</h3>
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
            <el-form-item >
                <el-button type="primary" @click="searchVibration" style="margin:auto">搜索</el-button>
            </el-form-item>
        </el-form>
    </div>

    <div id="main" style="width: 100%;height:500px;"></div>

</template>

<script setup>
    import { ref, onMounted } from 'vue'
    import router from "@/router/index.js"

    onMounted(()=>{
        // 向后端请求获取options
    })

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

    const formRef = ref(null);

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
    const selectedInfo = ref({
        'equipment': [],
        //数组：equipment[0]代表建筑，equipment[1]代表传感器编号
        'time': [],
        //时间数组：time[0]开始时间，time[1]是结束时间
    })

    const searchVibration = () =>{
        formRef.value.validate((valid) => {
            if(valid){   //表单验证成功
                let formData = new FormData();
                formData.append('building', selectedInfo.value.equipment[0])
                formData.append('equipment', selectedInfo.value.equipment[1])
                formData.append('start_time', selectedInfo.value.time[0])
                formData.append('end_time', selectedInfo.value.time[1])
                //发送请求

            }
            else{
                ElMessage.error('请检查表单是否填写正确！')
            }
        });
    }

    const change_select = () =>{
        console.log(selectedInfo.value.equipment)
        // console.log(selectedInfo.value.equipment[0])
    }

    const validateTime = (rule, value, callback) => {
        if(!value){
            callback(new Error('请选择时间'))
        }
        else{
            console.log(value);
            callback();
        }
    }

    const validateEquipment = (rule, value, callback) => {
        if(!value){
            callback(new Error('请选择建筑/传感器编号'))
        }
        else{
            callback();
        }
    }

    // 表单规则
    const fileRules = ref({
        time:[{
            validator:validateTime,
            trigger:'change',
        }],
        equipment:[{
            validator:validateEquipment,
            trigger:'change',
        }]
    })


</script>

<style scoped>

</style>