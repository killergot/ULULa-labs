<template>
  <div class="parent">
    <div class="div1">
      <button v-if="!editMode" class="edit-btn" @click="toggleEdit">Edit profile</button>
        <!-- ⚙️
      </button> -->

      <h1 v-if="!editMode">{{ user.fullName }}</h1>
      <div v-else class="edit-field">
        <label>Full name:</label>
        <input v-model="form.fullName" type="text" class="edit-input" />
      </div>


      <p v-if="!editMode">Group number: {{ user.group }}</p>
      <div v-else class="edit-field">
        <label>Group:</label>
        <select v-model="form.group" class="edit-input">
          <option value="" disabled>Выберите группу</option>
          <option
            v-for="g in groups"
            :key="g.id"
            :value="g.number"
          >
            {{ g.number }}
          </option>
        </select>
      </div>


      <p v-if="!editMode">Nickname: {{ user.nick }}</p>
      <div v-else class="edit-field">
        <label>Nickname:</label>
        <input v-model="form.nick" type="text" class="edit-input" />
      </div>

      <p v-if="!editMode">Email: {{ user.email }}</p>
      <div v-else class="edit-field">
        <label>Email:</label>
        <input v-model="form.email" type="email" class="edit-input" />
      </div>

      <p v-if="!editMode && user.telegram">
        Telegram:
        <a :href="'https://t.me/' + user.telegram" target="_blank">{{ user.telegram }}</a>
      </p>
      <div v-else class="edit-field">
        <label>Telegram:</label>
        <input v-model="form.telegram" type="text" class="edit-input" />
      </div>

      <div v-if="editMode" class="action-buttons">
        <button @click="cancelEdit">Cancel</button>
        <button @click="saveEdit">OK</button>
      </div>

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
 import api from '@/services/api';


export default {
  name: 'UserPage',
  data() {
    return {
      user: {
        fullName: 'Морозова Татьяна Сергеевна',
        group: '5151003/10801',
        nick: 'tanya-kiticat',
        email: 'morozovatania2003@yandex.ru',
        avatarUrl: '/my_sweet_cat.jpg',
        achievements: [
          'Дожила до 4 курса икизи',
          'Сдаю лабки' ,
          'Длиииииииииииииииииииииииииииииное очень длииииииииииииное достижение'
        ],
        telegram: 'tanya_kiticat', 
        // vk: 'tanya_morozova22'
      },
      editMode: false,
      form: {},
      groups: []
    }
  },
  created() {
    this.fetchGroups()
  },
  
  methods:{
    async fetchGroups() {
       try {
    const response = await api.get('/groups/get_all');

    if (response.status !== 200) throw new Error(`Error ${response.status}`);

    this.groups = response.data.map(group => ({
      id: group.group_id,
      number: group.group_number
    }));
  } catch (error) {
    console.error('Failed to fetch groups:', error);
  }
    },
    changeAvatar() {
        alert('здесь будет логика изменения аватара');
    },
    toggleEdit() {
      if (!this.editMode) {
        this.form = { ...this.user };
        this.editMode = true;
      } else {
        this.cancelEdit();
      }
    },
    saveEdit() {
      // Здесь можно отправить форму на сервер
      // Например: api.patch('/user/update', this.form)
      // После успешного ответа обновляем user
      this.user = { ...this.form };
      this.editMode = false;
    },
    cancelEdit() {
      this.form = {};
      this.editMode = false;
    }
  }
}

</script>
  
  

<style scoped>
.parent {
    display: grid;

    width: 100%;
    /* height: 100vh; */
    min-height: 100vh;
    padding: 16px;
    box-sizing: border-box;
    /* overflow-x: hidden; */

    overflow-x: auto;
    overflow-y: auto;

    /* grid-template-columns: 1fr 0.8fr 2px 1fr; */

    grid-template-columns:
    minmax(350px, 1fr)  
    minmax(350px, 0.8fr) 
    2px                  
    minmax(350px, 1fr);

    /* grid-template-rows: repeat(5, 1fr); */

    grid-template-rows: repeat(5, auto);
    gap: 8px;
}

.div1 {
  grid-column: 1 / 2;
  grid-row: 1 / 3;

  padding: 16px;
  box-sizing: border-box; 

  position: relative;
}

.div1 h1 {
  text-align: center;
  margin-top: 30px;
}

.div1 p {
  text-align: center;
  margin: 4px 0;
  margin-bottom: 10px; 
  
}

.edit-btn {
  position: absolute;
  top: 0;
  left: 0;
  z-index: 10;

  background-color: #79b9f5;
  border-radius: 4px;
  border: none;
  cursor: pointer;
  
  font-size: clamp(18px, 1.2vw, 22px);

  padding: clamp(4px, 1vh, 8px)
           clamp(8px, 1vw, 16px);

  min-width: 40px;
  min-height: 40px;

}
.edit-input {
  width: 100%;
  padding: 4px 8px;
  margin-top: 4px;
  margin-bottom: 12px;
  box-sizing: border-box;
  font-size: clamp(18px, 1.2vw, 22px);
}
.edit-field {
  margin-bottom: 12px;
}
.action-buttons {
  display: flex;
  gap: 8px;
  margin-top: 16px;
  justify-content: right;
}
.action-buttons button {
  padding: 8px 16px;
  border: none;
  background: #79b9f5;
  color: #0c0c0c;
  border-radius: 4px;
  cursor: pointer;
  font-size: clamp(18px, 1.2vw, 22px);
  
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
  font-size: clamp(18px, 1.2vw, 22px);
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
