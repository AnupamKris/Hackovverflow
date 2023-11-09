<template>
    <div class="post">
        <label for="">{{ post.author }}</label>
        <p>{{ post.content }}</p>

        <div class="comment-button">
            <ion-icon name="chatbox-outline"></ion-icon>
            <span @click="commentsOpen = !commentsOpen">Comment</span>
        </div>
        <div class="comments" v-if="commentsOpen">
            <div class="create-comment">
                <label for="">{{ user.user_data.name }}</label>

                <textarea v-model="comment" name="" id="" cols="30" rows="10" placeholder="Add a comment.."></textarea>
                <button @click="addComment">Post</button>
            </div>
            <div class="comment" v-for="comment in post.comments">
                <!-- {{ comment }} -->
                <label for="">{{ comment.author }}</label>
                <p>{{ comment.comment }}</p>
            </div>
        </div>
    </div>
</template>

<script setup>
import { ref } from 'vue'

const commentsOpen = ref(false)
const comment = ref("")

const props = defineProps({
    post: Object,
    user: Object
})

const addComment = () => {
    console.log("commenting");
    emit('update', { comment: comment.value, postid: props.post.id })
    comment.value = ""
}

const emit = defineEmits(['update'])

</script>

<style lang="scss" scoped>
.post {
    border-bottom: 2px solid #ececec;
    // padding: 20px 35px;
    display: flex;
    justify-content: center;
    align-items: center;
    flex-direction: column;

    padding: 20px 0;


    label {
        font-size: 18px;
        font-weight: 600;
        margin-bottom: 10px;
        width: 100%;
        padding: 5px 35px;
    }

    p {
        padding: 5px 35px;
        width: 100%;
        font-size: 14px;
        font-weight: 400;
        margin-bottom: 10px;
    }

    .comment-button {
        display: flex;
        align-items: center;
        // justify-content: center;
        width: 100%;
        padding: 10px;
        margin-bottom: 15px;
        background: #ececec;
        width: auto;
        margin-right: auto;
        margin-left: 20px;
        border-radius: 10px;


        ion-icon {
            font-size: 18px;
            margin-right: 10px;
        }

        span {
            font-size: 12px;
            font-weight: 600;
        }
    }


    .comments {
        display: flex;
        flex-direction: column;
        align-items: center;
        width: 100%;

        .comment {
            width: 100%;
            max-width: 1000px;
            border-bottom: 1px solid #ececec;
            margin-top: 10px;


            label {
                font-size: 16px;
                font-weight: 600;
                margin-bottom: 10px;
            }

            p {
                font-size: 12px;
                font-weight: 400;
                margin-bottom: 10px;
            }
        }

        .create-comment {
            width: 100%;
            max-width: 1000px;
            border-bottom: 1px solid #ececec;
            margin-top: 10px;
            padding: 10px 35px;
            display: flex;
            flex-direction: column;
            align-items: center;

            label {
                font-size: 18px;
                font-weight: 600;
                margin-bottom: 10px;
                padding: 0;
            }

            textarea {
                width: 100%;
                max-width: 1000px;
                height: 100px;
                border: 1px solid #ececec;
                outline: none;
                border-radius: 10px;
                padding: 10px;
                font-size: 16px;
                font-weight: 400;
                margin-bottom: 10px;
            }

            button {
                width: 100%;
                max-width: 1000px;
                height: 50px;
                border: none;
                outline: none;
                border-radius: 10px;
                background: #8844ff;
                color: #ffffff;
                font-size: 16px;
                font-weight: 600;
                margin-bottom: 10px;
            }
        }
    }


}
</style>