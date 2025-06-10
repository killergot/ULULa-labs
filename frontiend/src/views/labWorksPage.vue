<template>
  <div class="labWorkContainer">
    <div class="content">
      <h1 class="page-title">Laboratory work</h1>

      <div
        v-for="(subject, sIndex) in teacherSubjects"
        :key="subject.id"
        class="subject-block"
      >
        <div class="subject-header" @click="toggleSubject(sIndex)">
          <span class="subject-name">{{ subject.name }}</span>
          <span
            class="toggle-icon"
            :class="{ expanded: subject.expanded }"
          >❯</span>
        </div>

        <div v-if="subject.expanded" class="subject-content">
          <div
            v-for="(template, tIndex) in subject.templates"
            :key="template.id"
            class="template-block"
          >
            <div
              class="template-header"
              @click="toggleTemplate(sIndex, tIndex)"
            >
              <div class="template-info">
                <h3>{{ template.title }}</h3>
                <p>{{ template.description }}</p>
                <div v-if="template.file_id" class="file-link">
                  <span
                    class="file-item"
                    @click.stop="downloadTemplateFile(template)"
                    >Скачать материалы</span
                  >
                </div>
              </div>
              <div class="template-actions">
                <button class="action-btn" @click.stop="openAssignModal(template)">Выдать</button>
                <button class="icon-btn" @click.stop="openEditTemplateModal(template)">⋮</button>
                <button class="icon-btn" @click.stop="deleteTemplate(template)">✖</button>
              </div>
            </div>

            <hr class="separator" />

            <div v-if="template.expanded" class="assignments-list">
              <div
                v-for="group in groupedByDeadline(template.assignments)"
                :key="group.deadline"
                class="assignment-group"
              >
                <div class="assignment-deadline">
                  {{ formatDate(group.deadline) }}
                </div>
                <ul class="assignment-ul">
                  <li
                    v-for="assignment in group.items"
                    :key="assignment.id"
                    class="assignment-item"
                  >
                    <div class="assignment-info">
                      {{ assignment.group_number }}
                    </div>
                    <div class="assignment-actions">
                      <button
                        class="icon-btn"
                        @click.stop="editAssignment(assignment)"
                        >⋮</button
                      >
                      <button
                        class="icon-btn"
                        @click.stop="deleteAssignment(assignment)"
                        >✖</button
                      >
                    </div>
                  </li>
                </ul>
              </div>
            </div>
          </div>
        </div>
      </div>

      <button class="add-btn" @click="openCreateTemplateModal(null)">+</button>
    </div>
  </div>
</template>

<script>
import api from '@/services/api';

export default {
  name: 'LabWorkManager',
  data() {
    return {
      teacherSubjects: [],
      TEACHER_ROLE: 1,
      STUDENT_ROLE: 2,
      showCreateModal: false,
      showEditTemplateModal: false,
      showAssignModal: false,
      modalSubject: null,
      modalTemplate: null,
      modalAssignment: null,
    };
  },
  methods: {
    async fetchUser() {
      try {
        const userResp = await api.get('/users/get_me');
        if (userResp.data.role & this.TEACHER_ROLE) {
          await this.fetchTeacherSubjects();
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
        this.teacherSubjects = res.data.map(name => ({ name, id: null, expanded: false, templates: [] }));
        await Promise.all(
          this.teacherSubjects.map(async subj => {
            const idRes = await api.get(`/subjects/id/${encodeURIComponent(subj.name)}`);
            subj.id = idRes.data;
            await this.fetchTemplates(subj);
          })
        );
      } catch (error) {
        console.error(error);
      }
    },
    async fetchTemplates(subject) {
      try {
        const res = await api.get(
          `/teachers/lab_work/subject/${subject.id}?id=${subject.id}`
        );
        subject.templates = res.data.map(t => ({ ...t, expanded: false, assignments: [] }));
      } catch (error) {
        console.error(error);
      }
    },
    async fetchAssignments(template) {
      try {
        const res = await api.get(
          `/teachers/assignments/${template.id}?id=${template.id}`
        );
        template.assignments = await Promise.all(
          res.data.map(async a => {
            const numRes = await api.get(`/groups/get_group_number/${a.group_id}`);
            return { ...a, group_number: numRes.data };
          })
        );
      } catch (error) {
        console.error(error);
      }
    },
    async downloadTemplateFile(template) {
      if (!template.file_id) return;
      try {
        const response = await api.get(
          `/files/download/${template.file_id}`,
          { responseType: 'blob' }
        );
        if (response.status !== 200) throw new Error(`Error ${response.status}`);
        const url = window.URL.createObjectURL(new Blob([response.data]));
        const link = document.createElement('a');
        link.href = url;
        link.setAttribute('download', `lab_${template.id}`);
        document.body.appendChild(link);
        link.click();
        link.remove();
        window.URL.revokeObjectURL(url);
      } catch (error) {
        console.error(`Failed to download file for template ${template.id}:`, error);
      }
    },
    toggleSubject(i) {
      const subj = this.teacherSubjects[i];
      subj.expanded = !subj.expanded;
      if (subj.expanded) subj.templates.forEach(t => !t.assignments.length && this.fetchAssignments(t));
    },
    toggleTemplate(s, t) {
      const template = this.teacherSubjects[s].templates[t];
      template.expanded = !template.expanded;
      if (template.expanded && !template.assignments.length) this.fetchAssignments(template);
    },
    groupedByDeadline(items) {
      const groups = {};
      items.forEach(a => {
        (groups[a.deadline_at] = groups[a.deadline_at] || []).push(a);
      });
      return Object.entries(groups).map(([deadline, list]) => ({
        deadline,
        items: list
      }));
    },
    formatDate(d) {
      const dt = new Date(d);
      return `${String(dt.getDate()).padStart(2, '0')}-${String(
        dt.getMonth() + 1
      ).padStart(2, '0')}-${dt.getFullYear()}`;
    },
    openCreateTemplateModal(subject) {
      this.modalSubject = subject;
      this.showCreateModal = true;
    },
    openEditTemplateModal(template) {
      this.modalTemplate = template;
      this.showEditTemplateModal = true;
    },
    openAssignModal(template) {
      this.modalTemplate = template;
      this.showAssignModal = true;
    },
    editAssignment(a) {
      this.modalAssignment = a;
      this.showAssignModal = true;
    },
    deleteTemplate(t) {},
    deleteAssignment(a) {},
  },
  created() {
    this.fetchUser();
  },
};
</script>

<style scoped>
.labWorkContainer {
  position: relative;
  height: 100vh;
  overflow: hidden;
  min-width: 700px;
  overflow-x: auto;
}
.content {
  height: 100%;
  overflow-y: auto;
  background-color: #d9e2eb;
  padding: 16px 56px 16px;
}
.subject-block {
  margin-bottom: 24px;
}
.subject-header {
  background-color: #79b9f5;
  padding: 12px;
  cursor: pointer;
  position: relative;
  border-radius: 4px;
}
.subject-name {
  font-size: 20px;
  font-weight: bold;
  text-align: center;
  display: block;
}
.toggle-icon {
  position: absolute;
  right: 12px;
  top: 50%;
  transform: translateY(-50%);
  transition: transform 0.2s;
}
.toggle-icon.expanded {
  transform: translateY(-50%) rotate(90deg);
}
.template-block {
  background: white;
  margin: 12px 0;
  border-radius: 4px;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
}
.template-header {
  display: flex;
  justify-content: space-between;
  padding: 8px;
  cursor: pointer;
}
.template-info h3,
.template-info p {
  margin: 0;
  text-align: left;
}
.template-info h3 {
  text-align: left;
  width: 100%;
}
.template-actions {
  opacity: 0;
  display: flex;
  gap: 8px;
  transition: opacity 0.2s;
}
.template-header:hover .template-actions {
  opacity: 1;
}
.separator {
  border: none;
  border-top: 1px solid #ccc;
  margin: 0 8px;
}
.assignments-list {
  margin-left: 0;
}
.assignment-group {
  padding: 8px 8px;
  margin-bottom: 8px;
}
.assignment-deadline {
  font-weight: bold;
  margin-bottom: 4px;
}
.assignment-ul {
  padding-left: 8px;
  margin: 0;
}
.assignment-item {
  background: #f5f5f5;
  margin: 1px 0;
  padding: 8px;
  border-radius: 4px;
  display: flex;
  justify-content: space-between;
  align-items: center;
}
.assignment-actions {
  opacity: 0;
  display: flex;
  gap: 4px;
  transition: opacity 0.2s;
}
.assignment-item:hover .assignment-actions {
  opacity: 1;
}
.icon-btn {
  background: none;
  border: none;
  cursor: pointer;
  font-size: 18px;
  line-height: 1;
}
.action-btn {
  background-color: #46637f;
  color: white;
  border: none;
  border-radius: 4px;
  padding: 4px 8px;
  cursor: pointer;
}
.add-btn {
  position: absolute;
  right: 24px;
  bottom: 24px;
  width: 40px;
  height: 40px;
  border-radius: 10%;
  font-size: 24px;
  background: #46637f;
  color: white;
  border: none;
  cursor: pointer;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.2);
}
.file-link {
  margin-top: 8px;
  text-align: left;
}
.file-item {
  cursor: pointer;
  color: #007bff;
  text-decoration: underline;
}
.file-item:hover {
  color: #0056b3;
}
</style>
