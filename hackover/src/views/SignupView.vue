<template>
  <div class="signup">
    <div class="credentials" :class="activeTab == 0 ? 'active' : ''">
      <h1>Credentials</h1>
      <div class="input">
        <label for="name">Name</label>
        <input type="text" id="name" v-model="userData.name" />
      </div>
      <div class="input">
        <label for="email">Email</label>
        <input type="email" id="email" v-model="userData.email" />
      </div>
      <div class="input">
        <label for="password">Password</label>
        <input type="password" id="password" v-model="userData.password" />
      </div>
      <div class="input">
        <label for="phone">Phone</label>
        <input type="tel" id="phone" v-model="userData.phone" />
      </div>
      <div class="input">
        <button @click="activeTab = 1">
          <ion-icon name="arrow-forward-outline"></ion-icon>
        </button>
      </div>
      <div class="redirect">
        Already have an account? <RouterLink to="/login">Log In!</RouterLink>
      </div>
    </div>
    <div class="personal" :class="activeTab == 1 ? 'active' : ''">
      <h1>Personal Info</h1>

      <div class="input">
        <label for="dob">Date of Birth</label>
        <input type="date" id="dob" v-model="personalData.dob" />
      </div>
      <div class="input">
        <label for="hoursperday">Hours per day (In college)</label>
        <input
          type="number"
          id="hoursperday"
          v-model="personalData.hoursperday"
        />
      </div>
      <div class="input">
        <label for="yearofstudy">Year of Study</label>
        <input
          type="number"
          id="yearofstudy"
          v-model="personalData.yearofstudy"
        />
      </div>
      <div class="input">
        <label for="course">Course Of Study</label>
        <input type="text" id="course" v-model="personalData.course" />
      </div>
      <div class="input">
        <label for="hobbies">Hobbies (comma separated)</label>
        <input type="text" id="hobbies" v-model="personalData.hobbies" />
      </div>
      <div class="input">
        <label for="interests">Interests (comma separated)</label>
        <input type="text" id="interests" v-model="personalData.interests" />
      </div>
      <div class="input">
        <label for="stressbusters">Stress Busters (comma separated)</label>
        <input
          type="text"
          id="stressbusters"
          v-model="personalData.stressbusters"
        />
      </div>
      <div class="input split">
        <button @click="activeTab = 0">
          <ion-icon name="arrow-back-outline"></ion-icon>
        </button>
        <button @click="registerUser">
          <ion-icon name="checkmark-outline"></ion-icon>
        </button>
      </div>
      <div class="redirect">
        Already have an account? <RouterLink to="/login">Log In!</RouterLink>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from "vue";
import axios from "axios";
import { useRouter } from "vue-router";

const router = useRouter();

const apiUrl = "http://localhost:8000/";

const userData = ref({
  name: "",
  password: "",
  email: "",
  phone: "",
});

const personalData = ref({
  dob: "",
  hoursperday: "",
  yearofstudy: "",
  course: "",
  hobbies: "",
  interests: "",
  stressbusters: "",
});

const registerUser = () => {
  let postData = {
    user_data: userData.value,
    personal_data: personalData.value,
  };

  console.log(postData);

  axios
    .post(apiUrl + "register", postData)
    .then((res) => {
      console.log(res.data);
      router.push("/login");
    })
    .catch((err) => {
      console.log(err);
    });
};

const activeTab = ref(0);
</script>

<style lang="scss" scoped>
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
    width: 0%;
    max-width: 600px;
    // flex: 0;
    opacity: 0;
    transition: 0.3s;

    border: 2px solid #ececec;
    border-radius: 20px;
    height: auto;
    padding: 40px 0;

    * {
      transition: 0.3s;
    }

    .input {
      height: 90px;
      width: 0%;

      display: flex;
      justify-content: center;
      // align-items: center;
      flex-direction: column;

      label {
        margin-left: 0;
        color: #141414;
        // width: 0;
      }

      input {
        height: 50px;
        border: none;
        background: #ececec;
        border-radius: 10px;
        outline: none;
        padding: 0 0;
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

  .active {
    opacity: 1;
    width: 100%;

    .input {
      height: 90px;
      width: 70%;

      label {
        margin-left: 10px;
      }

      input {
        padding: 0 20px;
      }
    }
  }
}

.redirect {
  margin-top: 20px;
  font-size: 14px;
  color: #141414;

  a {
    color: #8844ff;
    text-decoration: none;
  }
}
</style>
