<template>
  <div class="parent">
    
    <div class="div1">
      <button class="edit-btn" :class="{ hidden: editMode }" @click="toggleEdit">✎</button>

      <div class="profile-info">
        <div class="main-fields">
        <template v-if="!editMode">
        <h1>{{ user.fullName || '–' }}</h1>
        <p v-if="isStudent"><span class="field-icon">🎓</span> Group number: {{ user.group || '–' }}</p>
        <p><span class="field-icon">👤</span> Nickname: {{ user.nick || '–' }}</p>
        <p><span class="field-icon">✉️</span> Email: {{ user.email || '–' }}</p>
        <p><span class="field-icon">💬</span> Telegram: <span v-if="user.telegram">
            <a :href="'https://t.me/' + user.telegram" target="_blank">{{ user.telegram }}</a>
          </span><span v-else>–</span>
        </p>
        </template>

        <template v-else>
          <div class="edit-field">
            <label>Full name</label>
            <input v-model="form.fullName" type="text" class="edit-input" />
          </div>
          <div v-if="isStudent" class="edit-field">
            <label >Group</label>
            <select v-model="form.group" class="edit-input">
              <option value="" disabled>Choose group</option>
              <option v-for="g in groups" :key="g.id" :value="g.number">
                {{ g.number }}
              </option>
            </select>
          </div>
          <div class="edit-field">
            <label>Nickname</label>
            <input v-model="form.nick" type="text" class="edit-input" />
          </div>
          <div class="edit-field">
            <label>Email</label>
            <input v-model="form.email" type="email" class="edit-input" />
          </div>
          <div class="edit-field">
            <label>Telegram</label>
            <input v-model="form.telegram" type="text" class="edit-input" />
          </div>
          <div class="action-buttons">
            <button @click="cancelEdit">Cancel</button>
            <button @click="saveEdit">OK</button>
          </div>
        </template>
        </div>

        <div class="security-section">
          <h2>Security</h2>
          <h3 class="sessions-title">Password</h3>
          <button class="security-btn" @click="handleChangePassword">Change Password</button>
          <h3 class="sessions-title">Sessions</h3>
          <div class="sessions-container">
            <div class="sessions-list">
              <div
                v-for="session in sessions"
                :key="session.id"
                class="session-item"
              >
                <span>{{ formatDate(session.created_at) }}</span>
                <span>Token: ...{{ shortToken(session.token) }}</span>
                <button @click="deleteSession(session.id)" class="delete-session">✕</button>
              </div>
            </div>
          </div>
        </div>

      </div>

      

    </div>



    <div class="div2">
      <div class="avatar-container">
        <img
          :src="user.avatarUrl || defaultAvatar"
          alt="Фото {{ user.fullName }}"
        />
      </div>

      <button @click="openModal">Change profile photo</button>
      <button @click="openDeleteModal" :disabled="!user.avatarUrl">Delete profile photo</button>

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

    <div v-if="showModal" class="modal-overlay">
      <div class="modal">
        <h2>Change Avatar</h2>
        <p>Enter the URL of the new avatar:</p>
        <textarea v-model="this.form.avatarUrl" class="modal-input" rows="3"></textarea>
        <div class="modal-actions">
          <button @click="closeModal">Cancel</button>
          <button @click="confirmModal">OK</button>
        </div>
      </div>
    </div>
    

    <div v-if="showDeleteModal" class="modal-overlay">
      <div class="modal">
        <h2>Delete Avatar</h2>
        <p>Are you sure you want to delete your profile photo?</p>
        <div class="modal-actions">
          <button @click="closeDeleteModal">Cancel</button>
          <button @click="confirmDelete">Delete</button>
        </div>
      </div>
    </div>

</div>
    
</template>
  
  
<script>
 import api from '@/services/api';
 const defaultAvatar = '/default_avatar.jpg';

  const TEACHER_ROLE = 1
  const STUDENT_ROLE = 2

export default {
  name: 'UserPage',
  data() {
    return {
      user: {
        fullName: '',
        group: '',
        nick: '',
        email: '',
        avatarUrl: null,
        achievements: [],
        telegram: ''
      },
      userRole: null,
      editMode: false,
      form: {},
      groups: [],     
      defaultAvatar,  
      showModal: false,
      showDeleteModal: false
    }
  },
  computed: {
    isStudent() { return this.userRole === STUDENT_ROLE; }
  },
  created() {
    this.fetchUser();
    this.fetchSessions();
  },
  
  methods:{
    async fetchUser() {
      try {
        const user_response = await api.get('/users/get_me');
        if (user_response.status !== 200) throw new Error(`Error ${user_response.status}`);
        this.userRole = user_response.data.role;

        if (this.userRole === STUDENT_ROLE) {
          const student_response = await api.get('/students/me');

          if (student_response.status !== 200) throw new Error(`Error ${student_response.status}`);

          this.user = {
            fullName: student_response.data.full_name,
            group: student_response.data.group_number,
            nick: student_response.data.nickname,
            email: student_response.data.email,
            avatarUrl: student_response.data.avatar_url,
            achievements: student_response.data.achievements,
            telegram: student_response.data.telegram
          };
        }
        else {
          const teacher_response = await api.get('/teachers/me');
          if (teacher_response.status !== 200) throw new Error(`Error ${teacher_response.status}`);
          
          this.user = {
            fullName: teacher_response.data.FIO,
            group: '',
            nick: teacher_response.data.nickname,
            email: teacher_response.data.email,
            avatarUrl: teacher_response.data.avatar_url,
            achievements: null,
            telegram: teacher_response.data.telegram
          };
        }
      } catch (error) {
        console.error('Failed to fetch user:', error);
      }        
    },

    async fetchSessions() {
      try {
        const response = await api.get('/users/my_sessions');
        if (response.status === 200) this.sessions = response.data;
      } catch (err) {
        console.error('Failed to fetch sessions:', err);
      }
    },

    async deleteSession(sessionId) {
      try {
        await api.delete(`/users/my_sessions/${sessionId}`);
        this.sessions = this.sessions.filter(s => s.id !== sessionId);
      } catch (err) {
        console.error('Failed to delete session:', err);
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

        if (this.isStudent) {
          const response = await api.put('/students/me', payload);

          if (response.status !== 200) throw new Error(`Error ${response.status}`);
          else {
            this.user = {
            fullName: response.data.full_name,
            group: response.data.group_number,
            nick: response.data.nickname,
            email: response.data.email,
            avatarUrl: response.data.avatar_url,
            achievements: response.data.achievements,
            telegram: response.data.telegram
          };

            console.log('User updated:', response.data);
          }
        }
        else {
          const response = await api.put('/teachers/me', payload);

          if (response.status !== 200) throw new Error(`Error ${response.status}`);
          else {
            this.user = {
            fullName: response.data.FIO,
            group: '',
            nick: response.data.nickname,
            email: response.data.email,
            avatarUrl: response.data.avatar_url,
            achievements: null,
            telegram: response.data.telegram
          };
            
            console.log('User updated:', response.data);
          }
        }

      } catch (error) {
        console.error('Failed to update user:', error);
      }
    },
    
    toggleEdit() {
      if (!this.editMode) {
        this.form = { ...this.user };
        this.editMode = true;
        this.fetchGroups();

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
    },
    openModal() {
      this.form = { ...this.user };
      this.showModal = true;
    },
    closeModal() {
      this.showModal = false;
      this.form = {};
    },
    async confirmModal() {
      await this.updateUser();
      this.closeModal();
    },
    openDeleteModal() {
      this.form = { ...this.user };
      this.showDeleteModal = true;
    },
    closeDeleteModal() {
      this.showDeleteModal = false;
      this.form = {};
    },
    async confirmDelete() {
      this.form.avatarUrl = null;
      await this.updateUser();
      this.closeDeleteModal();
    },
    formatDate(dateStr) {
    const date = new Date(dateStr);
    return date.toLocaleString(); 
  },
  shortToken(token) {
    if (!token) return '–';
    return token.slice(-10);
  }
  }
}

</script>
  
  

<style scoped>
.parent {
    display: grid;

    width: 100%;
    min-height: 100vh;
    padding: 16px;
    box-sizing: border-box;

    overflow-x: auto;
    overflow-y: auto;

    grid-template-columns:
    minmax(430px, 1fr)  
    minmax(350px, 0.8fr) 
    2px                  
    minmax(350px, 1fr);

    /* grid-template-rows: repeat(5, auto); */
    gap: 8px;

    background-color: #e3e9f0;
}

button {
  color: #003366;     
  font-weight: 600;   

}

.div1 {
  grid-column: 1 / 2;
  /* grid-row: 1 / 3; */

  padding: 16px;
  box-sizing: border-box; 
  position: relative;

  display: flex;
  flex-direction: column;
  height: 100%;

  display: grid; 
  grid-template-columns: auto 1fr; 
  column-gap: 16px;
}

.profile-info {
  flex: 1;
  display: flex;
  flex-direction: column;
}

.main-fields {
  flex-shrink: 0;
}

.profile-info h1 { 
  text-align: left; 
  margin-top: 0; 
  font-size: 2rem; 
}
.profile-info p { 
  display: flex; 
  align-items: center; 
  font-size: 1.3rem; 
  margin: 8px 0; 
  text-align: left; 
  margin: 4px 0;
  margin-bottom: 10px; 
  overflow-wrap: anywhere;
}

.field-icon { 
  margin-right: 8px; 
  flex: 0 0 auto;  
  font-size: 1.2rem; 
  align-self: flex-start;
}

.edit-field { 
  display: flex; 
  flex-direction: column; 
  align-items: flex-start; 
  margin-bottom: 12px; 
  font-size: 1.2rem; 
}
.edit-field label { 
  margin-bottom: 6px; 
  text-align: left; 
  width: 100%;
}
.edit-input { 
  width: 100%; 
  padding: 8px; 
  background-color: #f0f0f0; 
  border: 1px solid #ccc; 
  border-radius: 6px; 
  font-size: 1.2rem; 
}
.edit-btn {
  font-size: 1.8rem;
  visibility: visible;
  background: #79b9f5;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  align-self: start;   
  justify-self: start;
}
.edit-btn.hidden {
  visibility: hidden;
}
.edit-input {
  width: 100%;
  padding: 4px 8px;
  margin-top: 4px;
  margin-bottom: 12px;
  box-sizing: border-box;
  font-size: clamp(18px, 1.2vw, 22px);
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

.security-section {
  margin-top: 32px;
  margin-top: auto;
  /* background-color: #f1f1f1; */
  border-radius: 4px;
}

.security-section h2 {
  font-size: 1.5rem;
  margin-bottom: 12px;
}

.security-btn {
  background: #79b9f5;
  border: none;
  border-radius: 4px;
  padding: 8px 16px;
  font-size: clamp(14px, 1.2vw, 18px);
  cursor: pointer;
  margin-bottom: 24px;
  width: 100%;
}

.sessions-title {
  font-size: 1.2rem;
  margin: 0 8px 8px 8px;
  text-align: left;
}

.sessions-container {
  border: 1px solid #ccc;
  border-radius: 8px;
  padding: 12px;
  margin: 0 8px 16px 8px;
  height: 400px;
  overflow-y: auto;
  /* background-color: #e9e8e8; */
  background-color: #f1f1f1;
  max-height: 33vh;
}

.sessions-list {
  display: flex;
  flex-direction: column;
  gap: 8px;
  margin-top: 8px;
}

.session-item {
  display: flex;
  justify-content: space-between;
  align-items: center;

  font-size: 1.2rem;
  background: #fff;
  border: 1px solid #ccc;
  border-radius: 6px;
  padding: 8px 12px;
  margin-bottom: 8px;
  box-shadow: 0 1px 3px rgba(0,0,0,0.1);
  transition: background-color 0.2s ease;
}

.session-item:hover {
  background-color: #f0f8ff;
}

.delete-session {
  background: transparent;
  border: none;
  color: #cc0000;
  font-size: 1.2rem;
  cursor: pointer;
}

.div2 {
  grid-column: 2 / 3; 
  /* grid-row: 1 / 4; */

  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: flex-start;
  padding: 8px;
  box-sizing: border-box;
}

.avatar-container {

  border-radius: 4%;   
  overflow: hidden;
  margin-bottom: 12px;
}
.avatar-container img {
  width: 100%;
  height: 100%;
  max-height: 400px;
  object-fit: contain;
}

.div2 button {
  width: 100%;
  max-width: 100%;
  padding: 12px 0;
  margin-top: 12px;
  font-size: clamp(14px, 1.2vw, 18px);
  background-color: #79b9f5;
  border: none;
  border-radius: 6px;
  cursor: pointer;
  transition: background-color 0.3s;
}


.separator {
  grid-column: 3;
  /* grid-row: 1 / 6; */
  background-color: #ccc;
  width: 100%;
}

.div3 {
  grid-column: 4 / 5; 
  /* grid-row: 1 / 6; */
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


.modal-overlay { 
  position: fixed; 
  top: 0; 
  left: 0; 
  width: 100%; 
  height: 100%; 
  background: rgba(0,0,0,0.4); 
  display: flex; 
  align-items: center; 
  justify-content: center; 
  z-index: 1000; 
}
.modal { 
  background: #fff; 
  padding: 24px; 
  border-radius: 8px; 
  width: 90%; 
  max-width: 400px; 
  box-shadow: 0 4px 12px rgba(0,0,0,0.15); 
}
.modal h2 { 
  margin-top: 0; 
  margin-bottom: 12px; 
}
.modal p { 
  font-size: 1.2rem;
  margin-bottom: 8px; 
}
.modal-input { 
  width: 100%; 
  padding: 2px; 
  border: 1px solid #ccc; 
  border-radius: 4px; 
  resize: vertical; 
  min-height: 60px; 
  max-height: 200px;
  font-size: 1rem; 
  background-color: #f0f0f0;
}
.modal-actions { 
  display: flex; 
  justify-content: flex-end; 
  gap: 8px; 
  margin-top: 16px; 
}
.modal-actions button { 
  padding: 8px 16px; 
  border: none; 
  background: #79b9f5; 
  color: #fff; 
  border-radius: 4px; 
  cursor: pointer; 
  font-size: 1.1rem;
}
.modal-actions button:first-of-type { 
  background: #ccc; 
  color: #000; 
}
</style>
