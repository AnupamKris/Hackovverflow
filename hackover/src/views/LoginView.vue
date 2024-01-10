<template>
  <div class="signup">
    <div class="credentials">
      <h1>Login</h1>

      <div class="input">
        <label for="email">Email</label>
        <input type="email" id="email" v-model="userData.email" />
      </div>
      <div class="input">
        <label for="password">Password</label>
        <input type="password" id="password" v-model="userData.password" />
      </div>
      <span class="red" v-if="error"> Invalid Email or Password</span>
      <div class="input">
        <button @click="loginUser">Login</button>
      </div>
      <div class="redirect">
        Don't have an account? <RouterLink to="/signup">Sign Up!</RouterLink>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from "vue";
import axios from "axios";
import { useRouter } from "vue-router";
import { useUserStore } from "../stores/counter";

const { setToken, setUser, token, user } = useUserStore();

const apiUrl = "http://localhost:8000/";

const router = useRouter();

const userData = ref({
  password: "",
  email: "",
});
let error = ref(false);

const loginUser = () => {
  let postData = {
    email: userData.value.email,
    password: userData.value.password,
  };

  console.log(postData);

  axios
    .post(apiUrl + "login", postData)
    .then((res) => {
      console.log(res.data);
      setToken(res.data.token);
      setUser(res.data.user);
      console.log("AKSGHDKAJSLKLKJASD", user, token);
      router.push({ path: "hub" });
    })
    .catch((err) => {
      console.log(err);
      error.value = err;
    });
};

const activeTab = ref(0);
</script>

<style lang="scss" scoped>
.red {
  color: red;
}

.signup {
  height: 100%;
  width: 100%;

  scroll-snap-type: mandatory;
  background: #ffffff;
  display: flex;
  justify-content: center;
  align-items: center;

  .credentials,
  .personal {
    scroll-snap-align: start;
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    height: 100%;
    width: 70%;
    max-width: 600px;
    // flex: 0;
    opacity: 1;
    transition: 0.3s;

    border: 2px solid #ececec;
    height: auto;
    padding: 70px 0;
    border-radius: 10px;

    * {
      transition: 0.3s;
    }

    .redirect {
      margin-top: 20px;
      font-size: 16px;

      a {
        color: #8844ff;
        text-decoration: none;
      }
    }

    .input {
      height: 90px;
      width: 80%;

      display: flex;
      justify-content: center;
      // align-items: center;
      flex-direction: column;

      label {
        margin-left: 10px;
        // margin-left: 0;
        color: #141414;
        // width: 0;
      }

      input {
        height: 50px;
        border: none;
        background: #ececec;
        border-radius: 10px;
        outline: none;
        // padding: 0 0;
        padding: 0 20px;
        color: #141414;
      }
    }

    .split {
      display: flex;
      justify-content: space-between;
      align-items: center;
      flex-direction: row;

      button {
        width: 45%;
      }
    }

    button {
      height: 50px;
      border-radius: 10px;
      outline: none;
      border: none;
      background: #8844ff;
      color: #ffffff;

      font-size: 18px;
    }
  }
}
</style>
