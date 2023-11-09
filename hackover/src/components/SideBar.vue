<template>
    <div class="sidebar">
        <div class="logo">emot<p>i</p>on.<p>i</p>o</div>
        <div class="links">
            <RouterLink to="/chat">Chat</RouterLink>
            <RouterLink to="/hub">Social Hub</RouterLink>
            <RouterLink to="/profile">Profile</RouterLink>
            <RouterLink to="/dashboard">Reports</RouterLink>
        </div>
    </div>
</template>

<script setup>
import { RouterLink } from 'vue-router'


</script>

<style lang="scss" scoped>
.sidebar {
    width: 300px;
    height: 100%;

    display: flex;
    // justify-content: center;
    align-items: center;
    flex-direction: column;

    background: #ffffff;
    border-right: 1px solid #ececec;
    // margin-right: auto;

    position: absolute;
    left: 0;
    top: 0;

    .logo {
        font-size: 36px;
        font-weight: 600;
        margin-bottom: 20px;
        margin-top: 20px;
        display: flex;

        p {
            color: #8844ff;
        }
    }

    .links {
        width: 100%;
        max-width: 1000px;
        display: flex;
        flex-direction: column;
        align-items: center;

        a {
            width: 100%;
            max-width: 1000px;
            height: 60px;
            // border-radius: 25px;
            outline: none;
            border: none;
            // background: #8844ff;
            color: #141414;
            text-decoration: none;

            display: flex;
            // justify-content: center;
            align-items: center;

            font-size: 18px;
            font-weight: 600;

            padding: 0 20px;

            // margin-bottom: 10px;

            transition: 0.3s;

            &:hover {
                background: #e4e4e4;
            }
        }

        a.router-link-active {
            color: #8844ff;
        }
    }
}
</style>