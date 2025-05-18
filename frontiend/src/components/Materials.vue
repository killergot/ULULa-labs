<template>
  <div class="materials-list">
    <ul>
      <li v-for="subject in subjects" :key="subject.name" class="subject-item">
        <div class="subject-header" @click="toggleSubject(subject)">
          <span>{{ subject.name }}</span>
          <span class="toggle-icon" :class="{ rotated: subject.expanded }">❯</span>
        </div>
        <ul v-if="subject.expanded" class="files-list">
          <li
            v-for="file in subject.files"
            :key="file.id"
            class="file-item"
            @click="downloadFile(file)"
          >
            {{ file.filename }}
          </li>
        </ul>
      </li>
    </ul>
  </div>
</template>

<script>
import api from '@/services/api';

export default {
  name: 'MaterialsList',
  data() {
    return {
      user: {
        fullName: '',
        group_number: '',
        nick: '',
        email: '',
        avatarUrl: null,
        achievements: [],
        telegram: ''
      },
      subjects: []
    };
  },
  created() {
    this.fetchUser();
    this.fetchSubjects();
  },
  methods: {
    async fetchUser() {
      try {
        const response = await api.get('/students/me');
        if (response.status !== 200) throw new Error(`Error ${response.status}`);
        const data = response.data;
        this.user = {
          fullName: data.full_name,
          group_number: data.group_number,
          nick: data.nickname,
          email: data.email,
          avatarUrl: data.avatar_url,
          achievements: data.achievements,
          telegram: data.telegram
        };
      } catch (error) {
        console.error('Failed to fetch user:', error);
      }
    },
    async fetchSubjects() {
      try {
        const response = await api.get('/students/subjects');
        if (response.status !== 200) throw new Error(`Error ${response.status}`);
        this.subjects = response.data.map(name => ({ name, files: [], expanded: false }));
      } catch (error) {
        console.error('Failed to fetch subjects:', error);
      }
    },
    async fetchFilesForSubject(subject) {
      try {
        const params = {
          group_number: this.user.group_number,
          subject: subject.name
        };
        const response = await api.get('/files', { params });
        if (response.status !== 200) throw new Error(`Error ${response.status}`);
        subject.files = response.data;
      } catch (error) {
        console.error(`Failed to fetch files for ${subject.name}:`, error);
      }
    },
    toggleSubject(subject) {
      subject.expanded = !subject.expanded;
      if (subject.expanded && subject.files.length === 0) {
        this.fetchFilesForSubject(subject);
      }
    },
    async downloadFile(file) {
      try {
        const response = await api.get(`/files/download/${file.id}`, { responseType: 'blob' });
        if (response.status !== 200) throw new Error(`Error ${response.status}`);
        const url = window.URL.createObjectURL(new Blob([response.data]));
        const link = document.createElement('a');
        link.href = url;
        link.setAttribute('download', file.filename);
        document.body.appendChild(link);
        link.click();
        link.remove();
        window.URL.revokeObjectURL(url);
      } catch (error) {
        console.error(`Failed to download file ${file.filename}:`, error);
      }
    }
  }
};
</script>

<style scoped>
.materials-list {

  margin: 0 auto;
  font-family: sans-serif;
  overflow-x: hidden;
  overflow-y: auto;
}
.materials-list > ul {
  list-style: none;
  padding: 0;
  margin: 0;
}
.subject-item {
  margin-bottom: 10px;
}
.subject-header {
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: flex-start;
  background-color: #e6e6e6;
  padding: 8px;
  border-radius: 4px;
  text-align: left;
}
.toggle-icon {
  display: inline-block;
  transition: transform 0.3s ease;
  font-size: 1.2em;
  margin-left: auto;
}
.toggle-icon.rotated {
  transform: rotate(90deg);
}
.files-list {
  margin: 5px 0 0 15px;
  list-style-type: disc;
}
.file-item {
  cursor: pointer;
  margin: 3px 0;
  color: #007bff;
  text-decoration: underline;
  text-align: left;
  white-space: normal;
  word-break: break-word;
}
.file-item:hover {
  color: #0056b3;
}
</style>