<template>
  <SideBar />
  <div class="chat" v-if="token">
    <TransitionGroup name="chat-fade" tag="div" class="chats" ref="chatArea">
      <div class="chatarea">
        <div :class="msg.user" class="message" v-for="(msg, index) in messages">
          <p>{{ msg.message }}</p>
        </div>
      </div>
    </TransitionGroup>

    <div class="text-input">
      <div class="clear" @click="clearMessages">
        <ion-icon name="trash-outline"></ion-icon>
      </div>
      <input
        type="text"
        ref="inputRef"
        placeholder="Start Chatting..."
        v-model="message"
        @keyup.enter="addMessage"
        :disabled="messageRunning"
      />
      <div class="send" @click="addMessage">
        <ion-icon name="send-outline"></ion-icon>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from "vue";
import { useUserStore } from "../stores/counter";
import { useRouter } from "vue-router";
import axios from "axios";
import SideBar from "../components/SideBar.vue";
import { v4 } from "uuid";

const { user, token } = useUserStore();
const router = useRouter();
const apiUrl = "http://localhost:8000/chat";
const messages = ref([]);
const message = ref("");
const messageRunning = ref(false);
const inputRef = ref(null);
const chatid = ref();

const history = ref({
  internal: [["<|BEGIN-VISIBLE-CHAT|>", "How can I help you today?"]],
  visible: [["", "How can I help you today?"]],
});

const addMessage = () => {
  if (!message.value || messageRunning.value) return;
  let msg = {
    user: "user",
    message: message.value,
    timestamp: Date.now(),
  };
  messages.value.push(msg);
  message.value = "";
  messageRunning.value = true;

  let postData = {
    user_input: msg.message,
    history: history.value,
    email: user.user_data.email,
    chatid: chatid.value,
  };

  axios
    .post(apiUrl, postData)
    .then((res) => {
      let { history: his, reply } = res.data;
      let msg = {
        message: reply,
        user: "bot",
        timestamp: Date.now(),
      };

      messages.value.push(msg);
      history.value = his;
      console.log(history.value);
      messageRunning.value = false;
      inputRef.value.focus();
    })
    .catch((err) => {
      console.log(err);
      inputRef.value.focus();
    });

  // messageRunning.value = false
  // inputRef.value.focus()
};

const clearMessages = () => {
  messages.value = [];
  history.value = {
    internal: [["<|BEGIN-VISIBLE-CHAT|>", "How can I help you today?"]],
    visible: [["", "How can I help you today?"]],
  };
  chatid.value = v4();
};

onMounted(() => {
  if (!token) {
    console.log("no user");
    router.push("/login");
  } else {
    inputRef.value.focus();
    chatid.value = v4();
  }
});
</script>

<style lang="scss" scoped>
.chat {
  height: 100%;
  width: calc(100% - 400px);
  margin-left: 300px;
  display: flex;
  flex-direction: column;
  justify-content: space-around;
  align-items: center;

  background: #ffffff;

  .chats {
    height: calc(100% - 120px);
    overflow-y: scroll;
    width: calc(100% - 240px);
    max-width: 1200px;
    display: flex;
    background: #ececec;
    border-radius: 20px;
    flex-direction: column-reverse;

    &::-webkit-scrollbar {
      display: none;
    }

    /* Hide scrollbar for IE, Edge and Firefox */

    -ms-overflow-style: none;
    /* IE and Edge */
    scrollbar-width: none;
    /* Firefox */
  }

  .chatarea {
    * {
      transition: 0.3s;
    }

    height: auto;
    width: 100%;
    margin-top: 20px;

    padding: 0 20px;

    display: flex;
    // justify-content: center;
    align-items: center;
    flex-direction: column;

    .message {
      width: auto;
      max-width: 80%;
      background: #ffffff;
      border-radius: 15px 0 15px 15px;
      margin-bottom: 10px;
      padding: 10px 20px;
      min-height: 50px;
      border-bottom: 3px solid #8844ff;

      display: flex;
      flex-direction: column;
      justify-content: center;
      align-items: flex-start;

      span {
        font-size: 12px;
        color: #141414;
      }

      p {
        font-size: 16px;
        color: #141414;
      }
    }

    .user {
      border-bottom: 3px solid #425bff;
      margin-left: auto;
    }

    .bot {
      // border-bottom: 3px solid #ff44ff;
      margin-right: auto;
      border-radius: 0px 15px 15px 15px;
    }
  }

  .text-input {
    display: flex;
    justify-content: center;
    align-items: center;
    width: 60%;
    max-width: 1200px;
    height: 80px;

    .clear,
    .send {
      height: 50px;
      width: 50px;
      background: linear-gradient(180deg, #425bff 0%, #8844ff 100%);
      color: #ffffff;
      border-radius: 50%;
      display: flex;
      justify-content: center;
      align-items: center;

      margin: 0 10px;
    }

    input {
      height: 50px;
      width: 80%;
      border: 2px solid #ececec;
      background: #ececec;
      border-radius: 25px;
      outline: none;
      padding: 0 20px;
      color: #141414;
    }
  }
}

.chat-fade-move,
/* apply transition to moving elements */
.chat-fade-enter-active,
.chat-fade-leave-active {
  transition: all 0.5s ease;
}

.chat-fade-enter-from {
  opacity: 0;
  // transform: translate(-700px, 75px );
  transform: translate(-120px, 70px);

  // margin-right: auto;
  // left: 50px;
  .user {
    transform: translate(-120px, 0px);
  }
}

.chat-fade-leave-to {
  opacity: 0;
  height: 0;
  width: 0;
}

/* ensure leaving items are taken out of layout flow so that moving
   animations can be calculated correctly. */
.chat-fade-leave-active {
  position: absolute;
}
</style>
