<template>
  <div class="container">
    <label for="assignment-select" class="form-label">
        Choose laboratory work:
    </label>
    <div class="select-wrapper">
    <select id="assignment-select" v-model="selectedAssignmentId" @change="loadSubmissions" class="form-select">
        <option disabled value="">-- Choose submission --</option>
        <option
            v-for="assignment in assignments"
            :key="assignment.id"
            :value="assignment.id"
        >
            {{ assignment.title }} — group {{ assignment.group_number || assignment.group_id }}
        </option>
    </select>
    </div>

    <table v-if="submissions.length && !loadingSubmissions" class="submissions-table">
      <thead>
        <tr>
          <th>Student ID</th>
          <th>Status</th>
          <th>Mark</th>
          <th>Comment</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="submission in submissions" :key="submission.id">
          <td>{{ submission.student_id }}</td>
          <td>{{ statusText(submission.status) }}</td>
          <td>
            <input
              type="number"
              min="0"
              max="100"
              v-model.number="submission.mark"
            />
          </td>
          <td>
            <input
              type="text"
              v-model="submission.comment"
              placeholder="Комментарий"
            />
          </td>
        </tr>
      </tbody>
    </table>

    <button
      v-if="submissions.length"
      @click="saveAll"
      :disabled="saving"
      class="save-btn"
    >
      {{ saving ? 'Сохраняем...' : 'Save' }}
    </button>
  </div>
</template>

<script>
import api from '@/services/api';

export default {
  name: 'GradeSubmissions',
  data() {
    return {
      selectedAssignmentId: '',
      submissions: [],
      loadingSubmissions: false,
      saving: false,


      teacherSubjects: [],
      assignments: [],
      TEACHER_ROLE: 1, 
    };
  },
  async mounted() {
    await this.fetchUserAndData();
  },
  methods: {
    async fetchUserAndData() {
      try {
        const userResp = await api.get('/users/get_me');
        if (userResp.data.role & this.TEACHER_ROLE) {
          await this.fetchTeacherSubjects();
          this.collectAssignments();
        } else {
          this.$router.replace({ name: 'mainPage' });
        }
      } catch (e) {
        console.error(e);
      }
    },
    async fetchTeacherSubjects() {
      try {
        const res = await api.get('/teachers/subjects');
        this.teacherSubjects = res.data.map(name => ({ name, id: null, templates: [] }));
        await Promise.all(
          this.teacherSubjects.map(async subj => {
            const idRes = await api.get(`/subjects/id/${encodeURIComponent(subj.name)}`);
            subj.id = idRes.data;
            await this.fetchTemplates(subj);
          })
        );
        this.collectAssignments();
      } catch (error) {
        console.error(error);
      }
    },
    async fetchTemplates(subject) {
      try {
        const res = await api.get(`/teachers/lab_work/subject/${subject.id}?id=${subject.id}`);
        subject.templates = res.data.map(t => ({ ...t, assignments: [] }));
        await Promise.all(subject.templates.map(t => this.fetchAssignments(t)));
      } catch (error) {
        console.error(error);
      }
    },
    async fetchAssignments(template) {
        try {
            const res = await api.get(`/teachers/assignments/${template.id}?id=${template.id}`);
            template.assignments = await Promise.all(
            res.data.map(async a => {
                const numRes = await api.get(`/groups/get_group_number/${a.group_id}`);
                return { 
                ...a, 
                group_number: numRes.data, 
                lab_work_id: template.id,
                title: template.title
                };
            })
            );
        } catch (error) {
            console.error(error);
        }
        },
    collectAssignments() {
      this.assignments = [];
      this.teacherSubjects.forEach(subject => {
        subject.templates.forEach(template => {
          if (template.assignments && template.assignments.length) {
            this.assignments.push(...template.assignments);
          }
        });
      });
    },
    async loadSubmissions() {
      if (!this.selectedAssignmentId) {
        this.submissions = [];
        return;
      }
      this.loadingSubmissions = true;
      try {
        const res = await api.get(`/teachers/submissions/${this.selectedAssignmentId}?id=${this.selectedAssignmentId}`);
        this.submissions = res.data.map(sub => ({
          ...sub,
          mark: sub.mark || 0,
          comment: sub.comment || '',
        }));
      } catch (e) {
        console.error('Ошибка загрузки submissions:', e);
        alert('Не удалось загрузить работы студентов');
        this.submissions = [];
      } finally {
        this.loadingSubmissions = false;
      }
    },
    async saveAll() {
      if (!this.submissions.length) return;

      this.saving = true;
      try {
        await Promise.all(this.submissions.map(async (sub) => {

          await api.patch(`/teachers/submissions`, {
            id: sub.id,
            mark: sub.mark,
            comment: sub.comment,
            status: sub.status, 
          });
        }));
        alert('Оценки успешно сохранены');
      } catch (e) {
        console.error('Ошибка сохранения оценок:', e);
        alert('Ошибка при сохранении оценок');
      } finally {
        this.saving = false;
      }
    },
    statusText(status) {
    switch (status) {
      case 0:
        return 'not done';
      case 1:
        return 'done';
      default:
        return 'unknown';
    }
  },
  },
};
</script>

<style scoped>
.container {
  max-width: 700px;
  margin: 20px auto;
  font-family: Arial, sans-serif;
}
label {
  font-weight: bold;
}
select {
  margin: 10px 0 20px 0;
  padding: 6px;
  font-size: 16px;
}
.submissions-table {
  width: 100%;
  border-collapse: collapse;
  margin-bottom: 20px;
}
.submissions-table th,
.submissions-table td {
  border: 1px solid #ccc;
  padding: 8px;
  text-align: center;
}
.submissions-table input[type="number"],
.submissions-table input[type="text"] {
  width: 90%;
  padding: 4px;
  box-sizing: border-box;
}
.save-btn {
  padding: 8px 16px;
  background-color: #46637f;
  color: white;
  border: none;
  cursor: pointer;
  border-radius: 4px;
}
.save-btn:disabled {
  background-color: #a0a0a0;
  cursor: not-allowed;
}
.form-label {
  display: block;
  margin-bottom: 8px;
  text-align: center;
}
.select-wrapper {
  display: flex;
  justify-content: center; 
  margin-bottom: 20px;
}
.form-select {
  width: 300px; 
}
</style>
