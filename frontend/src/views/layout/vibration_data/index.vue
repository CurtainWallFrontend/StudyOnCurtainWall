<template>
    <div v-loading="loading">
        <el-button @click="GoToDash">进入仪表盘</el-button>

        <div v-if="true" style="width: 50%; margin: 30px auto;text-align: center;">
            <h3>选择条件进行数据查找</h3>
            <el-form label-width="auto" ref="formRef" :model="selectedInfo" :rules="fileRules">
                <!-- <el-form-item label="采集时间" prop="time">
                <el-date-picker
                    v-model="selectedInfo.time"
                    type="datetimerange"
                    range-separator="至"
                    start-placeholder="开始时间"
                    end-placeholder="结束时间"
                />
                </el-form-item> -->
                <el-form-item label="选择设备" prop="equipment">
                    <el-cascader v-model="selectedInfo.equipment" 
                        :options="options" 
                        placeholder="请选择建筑/传感器编号" 
                        @change="change_select" 
                        clearable/>
                </el-form-item>
                <el-form-item >
                    <el-button type="primary" @click="search" style="margin:auto">搜索</el-button>
                </el-form-item>
            </el-form>
        </div>

        <div style="width: 80%; margin: 30px auto;text-align: center;">
            <el-table 
                :data="tableData" 
                :default-sort="{ prop: 'last_modified', order: 'descending' }"
                border 
                style="width: 100%">
                <el-table-column prop="time"  label="采集时间" width="200px"/>
                <el-table-column prop="building" label="建筑" />
                <el-table-column prop="equipment" label="传感器" width="100px"/>
                <el-table-column prop="data" label="异常值" width="100px"/>
                <el-table-column prop="min" label="异常下限"/>
                <el-table-column prop="max" label="异常上限"/>
                <el-table-column prop="direction" label="方向" />
                <el-table-column prop="last_modified" sortable label="上次修改" width="200px"/>
            </el-table>
            <!-- 分页 -->
            <el-pagination class="pagination"
                background 
                v-model:currentPage="currentPage" 
                v-model:pageSize="pageSize" 
                :total="total"
            @current-change="handlePageChange" />
        </div>

        <div id="main" style="width: 100%;height:500px;"></div>
    </div>

</template>

<script setup>
    import { ref, onMounted } from 'vue'
    import { SearchAbnormal, GetDevice } from '@/api/vibration.js'
    import router from "@/router/index.js"

    const options = ref()
    const loading = ref(false) //加载

    onMounted(()=>{
        // 向后端请求获取options
        GetDevice()
        .then(function(result){
            options.value = result.data.options
        })
        .catch(function (error) {
            console.log(error);
        });
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

    const currentPage = ref(1); 
    const pageSize = ref(20);
    const total = ref(0);

    // 表格数据
    const tableData = ref()


    // 已选传感器信息
    const selectedInfo = ref({
        'equipment': [],
        //数组：equipment[0]代表建筑，equipment[1]代表传感器编号
        'time': [],
        //时间数组：time[0]开始时间，time[1]是结束时间
    })

    // 条件搜索
    const search = () =>{
        loading.value = true
        formRef.value.validate((valid) => {
            if(valid){   //表单验证成功
                let formData = new FormData();
                formData.append('building', selectedInfo.value.equipment[0]);
                formData.append('equipment', selectedInfo.value.equipment[1]);
                formData.append('start_time', selectedInfo.value.time[0]);
                formData.append('end_time', selectedInfo.value.time[1]);
                formData.append('pageNo', currentPage.value);
                formData.append('pageSize', pageSize.value);
                //发送请求
                SearchAbnormal(formData)
                .then(function(result){
                    total.value = result.data.total;
                    tableData.value = result.data.records;
                })
                .catch(function (error) {
                    console.log(error);
                })
                .finally(()=>{
                    loading.value = false;
                })
            }
            else{
                ElMessage.error('请检查表单是否填写正确！')
            }
        });
    }


    const change_select = () =>{
        // search();
    }


    const handlePageChange = () => {
        search();
        //调取后端获取数据库信息
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
    .pagination{
        margin-top:20px;
        margin-bottom:20px;
        justify-content: center;
        text-align:center;
    }
</style>