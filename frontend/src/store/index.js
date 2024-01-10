import { createStore } from 'vuex'
import createPersistedState from "vuex-persistedstate" //将 Vuex store 中的状态持久化到浏览器的本地存储

const store = createStore({
    plugins: [createPersistedState({
        storage: window.localStorage
    })],
    // 存放全局数据
    state: {
        username: '',
        email: '',
    },
    // 计算属性，获取state里的数据内容
    // 只可读取不可修改
    getters: {},
    // 定义对state的各种操作，只能同步不能异步
    mutations: {
        SET_USERNAME(state, payload) {
            state.username = payload
        },
        SET_EMAIL(state, payload) {
            state.email = payload
        },
        RESET_STATE(state) {
            state.username = ''
            state.email = ''
        }
    },   // 定义 mutations
    // 调用mmutations的操作，异步执行
    actions: {
        doLogout({ commit }) {
            commit('RESET_STATE')
        }
    },
    // state信息过长时，用以进行分割
    modules: {}
})


// 保存store状态到sessionStorage
function saveStateToSessionStorage() {
    sessionStorage.setItem('store', JSON.stringify(store.state))
}

// 在页面刷新前执行保存state到sessionStorage的操作
window.addEventListener('beforeunload', saveStateToSessionStorage)

export default store