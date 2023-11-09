<template>
    <SideBar />
    <div class="dashboard">
        <div class="health">
            <h2>Health Analysis</h2>
            <span class="block" v-for="data, index in analysisData">
                <div class="metrics">
                    <div class="row">
                        <p>Emotional State </p>
                        <span>{{ data.emotion }}</span>
                    </div>
                    <div class=" row">

                        <p>State Severity </p>
                        <span>{{ data.severity }}</span>
                    </div>
                    <div class=" row">
                        <p>Behaviour </p>
                        <span>{{ data.behaviour }}</span>
                    </div>
                </div>

                <div class=" report">
                    <p>Report</p>
                    <span>{{ data.report }}</span>
                </div>
            </span>
        </div>
    </div>
</template>

<script setup>
import { onMounted, ref } from 'vue';
import SideBar from '../components/SideBar.vue';
import { useUserStore } from '../stores/counter';
import { useRouter } from 'vue-router';
import axios from 'axios'

const router = useRouter();
const { user, token } = useUserStore()


const chats = ref([])
const analysisData = ref([])

const analyzeChat = (index) => {
    let history = chats.value[index]
    console.log(history)
    axios.post("http://192.168.137.55:8000/analyzeChat", { chat_history: history })
        .then(res => {
            console.log(res.data)
            let data = res.data

            data = data.replaceAll("**", "")
            data = data.replaceAll("*", "")
            data = data.split("\n")
            data = data.filter(d => d != "")

            let severity = data[0].split(":")[1]
            let emotion = data[1].split(":")[1]
            let behaviour = data[2].split(":")[1]

            let report = data[3]


            data = {
                severity,
                emotion,
                behaviour,
                report,

            }
            analysisData.value.push(data)
        })
        .catch(err => {
            console.log(err)
        })

}

const getChats = () => {
    axios.post("http://192.168.137.55:8000/getChats", { email: user.user_data.email })
        .then(res => {
            console.log(res.data)
            chats.value = res.data.filter(chat => chat.length > 2)

            chats.value.forEach((chat, index) => {
                analyzeChat(index)
                // console.log("ANANANNA", val);

            })
        })
        .catch(err => {
            console.log(err)
        })
}

onMounted(() => {
    console.log(user, token);
    if (!token) {
        console.log("no user");
        router.push('/login')
    } else {
        getChats()

    }
})
</script>

<style lang="scss" scoped>
.dashboard {
    height: 100%;
    width: calc(100% - 400px);
    margin-left: 300px;
    overflow-y: auto;


    .health {
        padding: 20px 0;

        .block {
            height: auto;
            width: 90%;
            border: 2px solid #ececec;

            display: flex;
            justify-content: center;
            align-items: center;
            flex-direction: column;
            border-radius: 10px;


            padding: 20px 0;
            margin-bottom: 20px;

            .metrics {
                width: 100%;
                display: flex;
                justify-content: space-around;
                align-items: center;
            }

            .row {
                width: 30%;

                display: flex;
                justify-content: center;
                align-items: center;
                flex-direction: column;

                background: #8844ff;
                color: #ffffff;
                height: 100px;
                padding: 10px 20px;
                border-radius: 10px;

                p {
                    font-size: 24px;
                    width: 100%;
                    font-weight: bold;
                }

                span {
                    font-size: 14px;
                    width: 100%;
                    font-weight: 400;
                }
            }



        }

        .report {
            display: flex;
            justify-content: center;
            align-items: center;
            flex-direction: column;

            width: 90%;
            margin-top: 20px;

            p {
                width: 100%;
                font-weight: 600;
                font-size: 18px;
            }
        }
    }
}
</style>