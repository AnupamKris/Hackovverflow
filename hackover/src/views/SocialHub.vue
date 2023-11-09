<template>
    <SideBar />
    <div class="hub">
        <div class="create" v-if="token">

            <label for="">{{ user.user_data.name }}</label>
            <textarea v-model="postContent" name="" id="" cols="30" rows="5" placeholder="What is happening?"></textarea>
            <div class="create-post-actions">
                <button @click="addPost">Post</button>
            </div>

        </div>
        <div class="posts">
            <Post v-for="post in posts" :post="post" @update="addComment" :user="user" />
        </div>
    </div>
</template>

<script setup>
import axios from 'axios'
import SideBar from '../components/SideBar.vue'
import { ref, onMounted } from 'vue'
import { useUserStore } from '../stores/counter';
import { useRouter } from 'vue-router';
import Post from '../components/Post.vue'
const url = "http://192.168.137.55:8000/"
const posts = ref([])
const { user, token, setToken, setUser } = useUserStore()
const router = useRouter();
const postContent = ref("")



onMounted(() => {
    console.log(user, token);
    if (!token) {
        console.log("no user");
        router.push('/login')
    }
    getposts()

})

const getposts = () => {
    axios.get(url + "getPosts")
        .then(res => {
            posts.value = res.data
        })
        .catch(err => {
            console.log(err)
        })
}

const addComment = ({ comment, postid }) => {
    console.log(comment, "aslkdja slkj", postid);
    let commentData = {
        "author": user.user_data.name,
        "comment": comment,
        "postid": postid
    }

    axios.post(url + "addComment", commentData)
        .then(res => {
            console.log(res.data)
            getposts()
        })
        .catch(err => {
            console.log(err)
        })
}

const addPost = () => {
    let postData = {
        "author": "AnupamKris",
        "content": postContent.value,
        "comments": []
    }

    axios.post(url + "addPost", postData)
        .then(res => {
            console.log(res.data)
            postContent.value = ""
            getposts()
        })
        .catch(err => {
            console.log(err)
        })
}


</script>

<style lang="scss" scoped>
.hub {
    height: 100%;
    width: calc(100% - 400px);
    margin-left: 300px;
    display: flex;
    // justify-content: center;
    align-items: center;
    flex-direction: column;
    overflow: scroll;


    .create {
        width: 100%;
        max-width: 1000px;
        height: 320px;
        display: flex;
        flex-direction: column;
        position: relative;

        border-left: 2px solid #ececec;
        border-right: 2px solid #ececec;
        border-bottom: 2px solid #ececec;

        padding: 0 35px;
        padding-bottom: 20px;
        padding-top: 20px;

        label {
            font-size: 18px;
            font-weight: 600;
            margin-bottom: 10px;
        }

        textarea {
            outline: none;
            border: 2px solid #ececec;

            background: #ffffff;
            border-radius: 10px;
            font-size: 14px;

            padding: 15px;

            // width: 90%;
        }

        button {
            height: 40px;
            border-radius: 20px;
            outline: none;
            border: none;
            background: #8844ff;
            color: #ffffff;

            width: 100px;
            // margin: 20px 0;

            font-size: 14px;
            font-weight: 600;
            position: absolute;

            bottom: 35px;
            right: 55px;
        }
    }

    .posts {
        border-left: 2px solid #ececec;
        border-right: 2px solid #ececec;

        height: auto;

        width: 100%;
        max-width: 1000px;



    }
}
</style>


