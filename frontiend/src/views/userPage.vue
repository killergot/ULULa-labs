<template>
  <div class="parent">
    <div class="div1">
        <h1>{{ user.fullName }}</h1>
        <p>Group number: {{ user.group }}</p>
        <p>Nickname:  {{ user.nick }}</p>

        <p v-if="user.telegram">Telegram: <a :href="'https://t.me/' + user.telegram" target="_blank">{{ user.telegram }}</a></p>
        <p v-if="user.vk">VK: <a :href="'https://vk.com/' + user.vk" target="_blank">{{ user.vk }}</a></p>
        
    </div>


    <div class="div2">
        <img :src="user.avatarUrl" alt="Фото {{ user.fullName }}" />
        <button @click="changeAvatar">Change profile photo</button>
    </div>

    <div class="separator"></div>

    <div class="div3">
        <h1>Achievements</h1>
        <ul>
            <li v-for="(ach, i) in user.achievements" :key="i">
                {{ ach }}
            </li>
        </ul>
        
    </div>


    
</div>
    
</template>
  
  
<script>
export default {
  name: 'UserPage',
  data() {
    return {
      user: {
        fullName: 'Морозова Татьяна Сергеевна',
        group: '5151003/10801',
        nick: 'tanya-kiticat',
        avatarUrl: '/my_sweet_cat.jpg',
        achievements: [
          'Дожила до 4 курса икизи',
          'Сдаю лабки' ,
          'Длиииииииииииииииииииииииииииииное очень длииииииииииииное достижение'
        ],
        telegram: 'tanya_kiticat', 
        vk: 'tanya_morozova22'
      }
    }
  },
  
  methods:{
    changeAvatar() {
        alert('здесь будет логика изменения аватара');
    }
  }
}

</script>
  
  

<style scoped>
.parent {
    display: grid;

    width: 100%;
    height: 100vh;
    padding: 16px;
    box-sizing: border-box;
    overflow-x: hidden;

    grid-template-columns: 1fr 0.8fr 2px 1fr;
    grid-template-rows: repeat(5, 1fr);
    gap: 8px;
}

.div1 {
  grid-column: 1 / 2;
  grid-row: 1 / 3;

  padding: 16px;
  box-sizing: border-box; 
}

.div1 p {
  text-align: center;
  margin: 4px 0;
  margin-bottom: 10px; 
}



.div2 {
  grid-column: 2 / 3; 
  grid-row: 1 / 4;

  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: flex-start;
  padding: 8px;
  box-sizing: border-box;
}

.div2 img {
  max-width: 100%;
  height: auto;
  display: block;

  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.div2 button {
  width: 100%;
  max-width: 100%;
  padding: 12px 0;
  margin-top: 12px;
  font-size: 1vw;
  background-color: #79b9f5;
  border: none;
  border-radius: 6px;
  cursor: pointer;
  transition: background-color 0.3s;
}


.separator {
  grid-column: 3;
  grid-row: 1 / 6;
  background-color: #ccc;
  width: 100%;
}

.div3 {
  grid-column: 4 / 5; 
  grid-row: 1 / 6;
}

.div3 ul {
  list-style: none; 
  padding-left: 0;
}

.div3 li {
  font-size: 18px;
  margin-bottom: 8px;
  line-height: 1.4;
  text-align: left;
  position: relative;
  padding-left: 28px; 
}

.div3 li::before {
  content: '🦉';
  position: absolute;
  left: 0;
  top: 0;
  font-size: 18px;
  line-height: 1.4;
}


</style>
