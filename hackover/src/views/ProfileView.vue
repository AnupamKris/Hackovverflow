<template>
    <SideBar />
    <div class="profile" v-if="token">
        <div class="row1">
            <div class="details">
                <div class="profile-pic">
                    <img src="https://picsum.photos/200/300?random=2" alt="" />
                </div>
                <div class="profile-details">
                    <p>{{ user.user_data.name }}</p>
                    <span>{{ user.user_data.email }}</span>
                </div>
            </div>
            <div class="personal">
                <p>Personal Details</p>
                <div class="personal-details">
                    <div class="detail">
                        <p>Phone</p>
                        <span>{{ user.user_data.phone }}</span>
                    </div>
                    <div class="detail">
                        <p>Date of Birth</p>
                        <span>{{ user.personal_data.dob }}</span>
                    </div>
                    <div class="detail">
                        <p>Course</p>
                        <span>{{ user.personal_data.course }}</span>
                    </div>
                    <div class="detail">
                        <p>Year of Study</p>
                        <span>{{ user.personal_data.yearofstudy }}</span>
                    </div>
                    <div class="detail">
                        <p>Hours per day</p>
                        <span>{{ user.personal_data.hoursperday }}</span>
                    </div>
                    <div class="detail">
                        <p>Hobbies</p>
                        <span>{{ user.personal_data.hobbies }}</span>
                    </div>
                    <div class="detail">
                        <p>Interests</p>
                        <span>{{ user.personal_data.interests }}</span>
                    </div>
                    <div class="detail">
                        <p>Stress Busters</p>
                        <span>{{ user.personal_data.stressbusters }}</span>
                    </div>
                </div>
            </div>
        </div>
        <div class="user_desc">{{ user.user_description.split(":")[1] }}</div>
        <!-- <div class="calendar">
            <p>Upcoming Events</p>
            <span class="events">
                <div class="event">
                    <ion-icon name="calendar-outline"></ion-icon>

                    <div class="event-det">
                        <p>Event Name</p>
                        <span>Event Date</span>
                    </div>
                </div>
                <div class="event"></div>
                <div class="event"></div>
                <div class="event"></div>
            </span>
        </div> -->
    </div>
</template>

<script setup>
import SideBar from '../components/SideBar.vue';
import { useUserStore } from '../stores/counter';
import { useRouter } from 'vue-router';
import { ref, onMounted } from 'vue'

const { user, token } = useUserStore()
const router = useRouter();

onMounted(() => {
    console.log(user, token);
    if (!token) {
        console.log("no user");
        router.push('/login')
    }
})

</script>

<style lang="scss" scoped>
.profile {
    height: 100%;
    width: calc(100% - 400px);
    margin-left: 300px;
    max-width: 1150px;
    display: flex;
    justify-content: center;
    align-items: center;
    flex-direction: column;


    .row1 {
        display: flex;
        justify-content: center;
        align-items: center;
        flex-direction: row;
        width: 100%;
        height: 400px;
    }

    .details {
        display: flex;
        flex-direction: column;
        justify-content: space-between;
        align-items: center;
        padding: 20px;
        border: 1px solid #ececec;
        border-radius: 10px;
        width: 350px;
        height: 100%;

        margin: 20px;

        .profile-pic {
            height: 250px;
            width: 250px;
            border-radius: 50%;
            overflow: hidden;

            img {
                height: 100%;
                width: 100%;
                object-fit: cover;
            }
        }

        .profile-details {
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: flex-start;


            p {
                font-size: 1.5rem;
                font-weight: 600;
            }

            span {
                font-size: 1rem;
                font-weight: 400;
            }
        }
    }

    .personal {
        display: flex;
        flex-direction: column;
        justify-content: space-between;
        align-items: center;
        padding: 20px;
        border: 1px solid #ececec;
        border-radius: 10px;
        width: calc(100% - 400px);
        height: 100%;

        margin: 20px;

        p {
            font-size: 24px;
            font-weight: 800;
            width: 100%;
        }

        .personal-details {
            display: grid;
            grid-template-columns: repeat(2, 1fr);
            gap: 5px;


            p {
                font-size: 16px;
                font-weight: 600;
            }

            span {
                font-size: 14px;
                font-weight: 400;
            }

            .detail {
                display: flex;
                flex-direction: column;
                justify-content: center;
                align-items: flex-start;
                margin: 10px 0;
            }
        }
    }

    .user_desc,
    .calendar {
        display: flex;
        justify-content: center;
        align-items: center;

        width: calc(100% - 40px);
        height: 120px;
        margin: 20px;
        border: 1px solid #ececec;
        border-radius: 10px;

        padding: 0 20px;
    }

    .calendar {
        margin-top: 0;
        display: flex;
        justify-content: space-around;
        align-items: center;
        flex-direction: column;

        p {
            font-size: 18px;
            font-weight: 600;
            width: 100%;
        }

        .events {
            display: flex;
            justify-content: space-between;
            align-items: center;
            width: 100%;

            .event {
                height: 50px;
                border: 1px solid #ececec;
                width: 180px;
                border-radius: 10px;

                display: flex;
                justify-content: space-around;
                align-items: center;

                ion-icon {
                    width: 40px;
                }

                .event-det {
                    display: flex;
                    justify-content: center;
                    align-items: center;
                    flex-direction: column;
                    margin-left: 10px;
                    width: calc(100% - 50px);

                    p {
                        font-size: 14px;
                        font-weight: 600;
                        width: 100%;
                    }

                    span {
                        font-size: 12px;
                        width: 100%;
                        font-weight: 400;
                    }
                }
            }
        }
    }
}
</style>