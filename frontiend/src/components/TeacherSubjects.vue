<template>
  <div class="subjects-list">

    <div class="add-subject">
      <select v-model="newSubjectName">
        <option disabled value="">Select subject to add</option>
        <option v-for="subj in allSubjects" :key="subj.id" :value="subj.name">
          {{ subj.name }}
        </option>
      </select>
      <button @click="addSubject" :disabled="!newSubjectName">Add subject</button>
    </div>

    <ul class="subjects-ul">
      <li v-for="subject in teacherSubjects" :key="subject.name" class="subject-item">
        <div class="subject-header" @click="toggleSubject(subject)">
          <span>{{ subject.name }}</span>
          <span class="toggle-icon" :class="{ rotated: subject.expanded }">❯</span>
        </div>
        <div v-if="subject.expanded" class="groups-list">

          <div v-for="group in subject.groups" :key="group.name" class="group-item">
            <div class="group-header" @click="toggleGroup(subject, group)">
              <span>{{ group.name }}</span>
              <span class="toggle-icon" :class="{ rotated: group.expanded }">❯</span>
            </div>

            <ul v-if="group.expanded" class="files-list">
              <li v-for="file in group.files" :key="file.id" class="file-item" @click="downloadFile(file)">
                {{ file.filename }}
              </li>

              <li class="add-file">
                <div v-if="group.showFileInput">
                  <input
                    ref="fileInput"
                    type="file"
                    multiple 
                    @change="onFileSelected($event, subject, group)"
                  />
                  <button @click="uploadSelectedFile(subject, group)">Upload</button>
                </div>
                <div v-else>
                  <button @click="showUploadInputs(group)">Add file</button>
                </div>
              </li>
            </ul>
          </div>
        </div>
      </li>
    </ul>
  </div>
</template>

<script>
import api from '@/services/api';

export default {
  name: 'TeacherSubjectsList',
  data() {
    return {
      allSubjects: [],
      teacherSubjects: [],
      newSubjectName: '',
      selectedFiles: {}
    };
  },
  async created() {
    await this.fetchAllSubjects();
    await this.fetchTeacherSubjects();
  },
  methods: {
    async fetchAllSubjects() {
      try {
        const res = await api.get('/subjects');
        if (res.status !== 200) throw new Error(`Error ${res.status}`);
        this.allSubjects = res.data;
      } catch (error) {
        console.error('Failed to fetch all subjects:', error);
      }
    },
    async fetchTeacherSubjects() {
      try {
        const res = await api.get('/teachers/subjects');
        if (res.status !== 200) throw new Error(`Error ${res.status}`);
        this.teacherSubjects = res.data.map(name => ({
          name,
          expanded: false,
          groups: []
        }));
      } catch (error) {
        console.error('Failed to fetch teacher subjects:', error);
      }
    },
    async addSubject() {
      try {
        const res = await api.post('/teachers/subject', { name: this.newSubjectName });
        if (res.status !== 201) throw new Error(`Error ${res.status}`);
        await this.fetchTeacherSubjects();
        this.newSubjectName = '';
      } catch (error) {
        console.error('Failed to add subject:', error);
      }
    },
    async toggleSubject(subject) {
      subject.expanded = !subject.expanded;
      if (subject.expanded && subject.groups.length === 0) {
        try {
          const res = await api.get(`/subjects/groups/${encodeURIComponent(subject.name)}`);
          if (res.status !== 200) throw new Error(`Error ${res.status}`);
          subject.groups = res.data.map(name => ({
            name,
            expanded: false,
            files: [],
            showFileInput: false
          }));
        } catch (error) {
          console.error(`Failed to fetch groups for ${subject.name}:`, error);
        }
      }
    },
    async toggleGroup(subject, group) {
      group.expanded = !group.expanded;

      if (!group.expanded) {
        group.showFileInput = false; 
        return;
  }

      if (group.expanded && group.files.length === 0) {
        try {
          const params = { group_number: group.name, subject: subject.name };
          const res = await api.get('/files', { params });
          if (res.status !== 200) throw new Error(`Error ${res.status}`);
          group.files = res.data;
        } catch (error) {
          console.error(`Failed to fetch files for group ${group.name}:`, error);
        }
      }
    },
    downloadFile(file) {
      api.get(`/files/download/${file.id}`, { responseType: 'blob' })
        .then(resp => {
          if (resp.status !== 200) throw new Error(`Error ${resp.status}`);
          const url = URL.createObjectURL(new Blob([resp.data]));
          const a = document.createElement('a');
          a.href = url;
          a.download = file.filename;
          document.body.appendChild(a);
          a.click();
          a.remove();
          URL.revokeObjectURL(url);
        })
        .catch(error => console.error(`Download failed for ${file.filename}:`, error));
    },
    onFileSelected(event, subject, group) {
      const files = Array.from(event.target.files);
      const key = `${subject.name}-${group.name}`;
      this.selectedFiles[key] = files;
  },
  async uploadSelectedFile(subject, group) {
    const key = `${subject.name}-${group.name}`;
    const files = this.selectedFiles[key];
    if (!files || files.length === 0) return;

    const form = new FormData();
    files.forEach(file => {
      form.append('files', file); 
    });
    form.append('group_number', group.name);
    form.append('subject', subject.name);

    try {
      const res = await api.post('/files', form, {
        headers: { 'Content-Type': 'multipart/form-data' }
      });
      if (res.status !== 201) throw new Error(`Error ${res.status}`);


      const fileRes = await api.get('/files', {
        params: { group_number: group.name, subject: subject.name }
      });
      if (fileRes.status !== 200) throw new Error(`Error ${fileRes.status}`);
      group.files = fileRes.data;

      delete this.selectedFiles[key];
      group.showFileInput = false; 
    } catch (error) {
      console.error(`Failed to upload files for group ${group.name}:`, error);
    }
  },
  showUploadInputs(group) {
    group.showFileInput = true;
  }
  }
};
</script>

<style scoped>
.subjects-list {
  margin: 0 auto;
  font-family: sans-serif;
  text-align: left;
  display: flex;
  flex-direction: column;
  height: 100%;
  overflow-x: auto;
  min-width: 400px;
}
.add-subject {
  display: flex;
  gap: 8px;
  margin-bottom: 16px;
}
button {
  border-radius: 4px;
  background-color: #79b9f5;
  color: black;
  font-size: 16px;
  border: none;
  padding: 6px 12px;
  cursor: pointer;
  transition: background 0.3s ease;
}
button:hover {
  background-color: #5ea6eb;
}
.add-subject select {
  flex-grow: 1;
  box-sizing: border-box;
  max-width: 300px;
}
.add-subject button {
  flex: none;
  width: auto;
  white-space: nowrap;
}
.subjects-ul {
  list-style: none;
  padding: 0;
  margin: 0;
}
.subject-item {
  margin-bottom: 10px;
}
.subject-header,
.group-header {
  cursor: pointer;
  display: flex;
  align-items: center;
  background: #dce9f9 ;
  padding: 8px;
  border-radius: 4px;
  text-align: left;
  list-style: none;
}
.group-header {
  background: #e6e6e6;
}
.toggle-icon {
  margin-left: auto;
  transition: transform 0.3s ease;
}
.toggle-icon.rotated {
  transform: rotate(90deg);
}
.groups-list {
  margin: 5px 0 0 15px;
}
.group-item {
  margin-bottom: 8px;
}
.files-list {
  list-style: disc;
  margin: 5px 0 0 30px;
  padding: 0;
}
.file-item {
  cursor: pointer;
  margin: 3px 0;
  color: #007bff;
  text-decoration: underline;
  white-space: normal;
  word-break: break-word;
}
.file-item:hover {
  color: #0056b3;
}
.add-file {
  margin-top: 8px;
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.add-file input[type="file"] {
  width: 100%;
}
</style>