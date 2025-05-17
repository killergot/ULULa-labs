<template>
  <div class="parent">
    <div class="div1">
      <button v-if="!editMode" class="edit-btn" @click="toggleEdit">Edit profile</button>
        <!-- ⚙️
      </button> -->

      <h1 v-if="!editMode">{{ user.fullName || '–' }}</h1>
      <div v-else class="edit-field">
        <label>Full name:</label>
        <input v-model="form.fullName" type="text" class="edit-input" />
      </div>


      <p v-if="!editMode">Group number: {{ user.group || '–' }}</p>
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


      <p v-if="!editMode">Nickname: {{ user.nick || '–' }}</p>
      <div v-else class="edit-field">
        <label>Nickname:</label>
        <input v-model="form.nick" type="text" class="edit-input" />
      </div>

      <p v-if="!editMode">Email: {{ user.email || '–' }}</p>
      <div v-else class="edit-field">
        <label>Email:</label>
        <input v-model="form.email" type="email" class="edit-input" />
      </div>

      <p v-if="!editMode">
        Telegram:
        <span v-if="user.telegram">
          <a :href="'https://t.me/' + user.telegram" target="_blank">{{ user.telegram }}</a>
        </span>
        <span v-else>–</span>
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




    <!-- <div class="div2">
        <img :src="user.avatarUrl" alt="Фото {{ user.fullName }}" />
        <button @click="changeAvatar">Change profile photo</button>
    </div> -->

    <div class="div2">
      <div class="avatar-container">
        <!-- Если есть локальное превью, покажем его,
            иначе — или то, что в базе, или дефолт -->
        <img
          :src="previewUrl || user.avatarUrl || defaultAvatar"
          alt="Фото {{ user.fullName }}"
        />
      </div>
      <button @click="onClickChange">Change profile photo</button>
      <input
        ref="fileInput"
        type="file"
        accept="image/*"
        @change="onFileSelected"
        style="display: none;"
      />
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
 const defaultAvatar = '/default_avatar.jpg';


export default {
  name: 'UserPage',
  data() {
    return {
      user: {
        fullName: '',
        group: '',
        nick: '',
        email: '',
        avatarUrl: '',
        achievements: [],
        telegram: ''
      },
      editMode: false,
      form: {},
      groups: [],
      previewUrl: null,     
      defaultAvatar,  
    }
  },
  created() {
    this.fetchUser();
    this.fetchGroups();
  },
  
  methods:{
    async fetchUser() {
      try {
        const response = await api.get('/students/me');

        if (response.status !== 200) throw new Error(`Error ${response.status}`);

        this.user = {
          fullName: response.data.full_name,
          group: response.data.group_number,
          nick: response.data.nickname,
          email: response.data.email,
          avatarUrl: response.data.avatar_url || null,
          achievements: response.data.achievements || [],
          telegram: response.data.telegram
        };
      } catch (error) {
        console.error('Failed to fetch user:', error);
      }
    },


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

    async updateUser() {
      try {
        const payload = {
          group_number: this.form.group || null,
          full_name: this.form.fullName || null,
          email: this.form.email || null,
          telegram: this.form.telegram || null,
          avatar_url: this.form.avatarUrl || null,
          nickname: this.form.nick || null
        };

        const response = await api.put('/students/me', payload);

        if (response.status !== 200) throw new Error(`Error ${response.status}`);
        else {
          this.user = {
          fullName: response.data.full_name,
          group: response.data.group_number,
          nick: response.data.nickname,
          email: response.data.email,
          avatarUrl: response.data.avatar_url || null,
          achievements: response.data.achievements || [],
          telegram: response.data.telegram
        };
          console.log('User updated:', response.data);
        }

      } catch (error) {
        console.error('Failed to update user:', error);
      }
    },

    onClickChange() {
      this.$refs.fileInput.click();
    },

    changeAvatar() {
        alert('здесь будет логика изменения аватара');
      //   const file = e.target.files[0];
      // if (!file) return;

      // // 1) Локальное превью
      // this.previewUrl = URL.createObjectURL(file);

      // // 2) Загружаем на сервер
      // const form = new FormData();
      // form.append('avatar', file);
      // try {
      //   const { status, data } = await api.post(
      //     '/students/me/avatar',
      //     form,
      //     { headers: { 'Content-Type': 'multipart/form-data' } }
      //   );
      //   if (status === 200 && data.avatar_url) {
      //     // 3) После успеха обновляем у себя и сбрасываем превью
      //     this.user.avatarUrl = data.avatar_url;
      //     this.previewUrl = null;
      //   } else {
      //     throw new Error(`Upload failed: ${status}`);
      //   }
      // } catch (err) {
      //   console.error(err);
      //   // Можно показать уведомление об ошибке
      // }
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
      this.updateUser();
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

.avatar-container {
  width: 150px;
  height: 150px;
  border-radius: 50%;   
  overflow: hidden;
  margin-bottom: 12px;
}
.avatar-container img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

/* .div2 img {
  max-width: 100%;
  height: auto;
  display: block;

  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
} */

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
