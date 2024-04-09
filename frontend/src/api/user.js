// 管理用户数据
import { defineStore } from "pinia"
import { ref } from "vue"
import store from '@/store/index.js'
import Request from "@/utils/Request.js";  // 在每个 api 文件里都要引入这两个文件
import Message from "@/utils/Message.js"  // 在每个 api 文件里都要引入这两个文件

export const useUserStore = defineStore('user', () => {
    const userInfo = ref({});

    const login = async (email, password) => {
        try {
            const response = await Request.post('/login', { "username": email, "password": password });
            if (response.status === 200) {
                // 存储Token和email到localStorage
                localStorage.setItem('authToken', response.data.token);
                localStorage.setItem('email', email);
                userInfo.value = response.data;
                return true;
            } else {
                console.error(response);
            }
        } catch (error) {
            Message.error(error.message)
        }
    };

    const sendVerificationCode = async (email) => {
        try {
            const response = await Request.post('/register', { "email": email });
            if (response.status === 200) {
                Message.success(response.data.message);
                return true;
            } else {
                console.error(response);
                return false;
            }
        } catch (error) {
            Message.error(error.message);
            return false;
        }
    };

    const register = async (email, code, password) => {
        try {
            const response = await Request.post('/validate', { "email": email, "code": code, "password": password });
            if (response.status === 200) {
                Message.success(response.data.message);
                return true;
            } else {
                console.error(response);
                return false;
            }
        } catch (error) {
            Message.error(error.message);
            return false;
        }
    };

    const getCurrentInfo = async (user) => {
        try {
            const headers = { 'Authorization': `Token ${user}` };
            const response = await Request.get('/get-info', { headers });
            if (response.status === 200) {
                // Message.success(response.data.message);
                return response.data.data;
            } else {
                console.error(response);
                return response.data;
            }
        } catch (error) {
            Message.error(error.message);
            return response.data;
        }
    };

    // 退出时清除用户信息
    const clearUserInfo = () => {
        userInfo.value = {};
        store.dispatch('doLogout');
    };

    return {
        userInfo,
        sendVerificationCode,
        login,
        register,
        clearUserInfo,
        getCurrentInfo
    };
}, {
    persist: true,
});
