<template>
  <div class="task-manager">
    <div class="content" :class="{ blurred: showAddModal || showEditModal }">

    <!-- Important -->
    <section class="section">
      <header @click="collapsedImportant = !collapsedImportant">
        <h2>Important tasks</h2>
        <span class="toggle-icon" :class="{ rotated: !collapsedImportant }">❯</span>
      </header>
      <transition name="collapse">
        <div v-show="!collapsedImportant" class="section-content">
          <template v-for="(tasks, date) in groupedImportant" :key="date">
            <h3 v-if="date">{{ formatDate(date) }}</h3>
            <ul>
              <li
                v-for="task in tasks"
                :key="task.id"
                class="task-item"
                :class="{ completed: task.completed, urgent: isUrgent(task) }"
              >
                <label>
                  <input type="checkbox" :checked="task.completed" @change="toggleComplete(task)" />
                </label>
                <span class="task-text">{{ task.text }}</span>
                <div class="more-actions">
                  <button
                    class="share-btn"
                    @click="shareTask(task)"
                    title="Share"
                  >
                    🔗
                  </button>
                  <button @click="openEditModal(task)">⋮</button>
                </div>
              </li>
            </ul>
          </template>
        </div>
      </transition>
    </section>

    <!-- Tasks -->
    <section class="section">
      <header @click="collapsedOthers = !collapsedOthers">
        <h2>Tasks</h2>
        <span class="toggle-icon" :class="{ rotated: !collapsedOthers }">❯</span>
      </header>
      <transition name="collapse">
        <div v-show="!collapsedOthers" class="section-content">
          <template v-for="(tasks, date) in groupedOthers" :key="date">
            <h3 v-if="date">{{ formatDate(date) }}</h3>
            <ul>
              <li
                v-for="task in tasks"
                :key="task.id"
                class="task-item"
                :class="{ completed: task.completed, urgent: isUrgent(task) }"
              >
                <label>
                  <input type="checkbox" :checked="task.completed" @change="toggleComplete(task)" />
                </label>
                <span class="task-text">{{ task.text }}</span>
                <div class="more-actions">
                  <button
                    class="share-btn"
                    @click="shareTask(task)"
                    title="Share"
                  >
                    🔗
                  </button>
                  <button @click="openEditModal(task)">⋮</button>
                </div>
              </li>
            </ul>
          </template>
        </div>
      </transition>
    </section>

    <section class="section">
      <header @click="collapsedCompleted = !collapsedCompleted">
        <h2>Completed tasks</h2>
        <span class="toggle-icon" :class="{ rotated: !collapsedCompleted }">❯</span>
      </header>
      <transition name="collapse">
        <div v-show="!collapsedCompleted" class="section-content">
          <template v-for="(tasks, date) in groupedCompleted" :key="date">
            <h3 v-if="date">{{ formatDate(date) }}</h3>
            <ul>
              <li v-for="task in tasks" :key="task.id" class="task-item completed">
                <label>
                  <input type="checkbox" checked @change="toggleComplete(task)" />
                </label>
                <span class="task-text">{{ task.text }}</span>
                <div class="more-actions">
                  <button
                    class="share-btn"
                    @click="shareTask(task)"
                    title="Share"
                  >
                    🔗
                  </button>
                  <button @click="openEditModal(task)">⋮</button>
                </div>
              </li>
            </ul>
          </template>
        </div>
      </transition>
    </section>

  </div>



    <button class="add-btn" @click="openAddModal">+</button>


    <div v-if="showAddModal || showEditModal" class="modal-overlay">
      <div class="modal">

        <h3 class="modal-title">
          {{ showAddModal ? 'New task' : 'Edit task' }}
        </h3>


        <textarea
          v-model="modalData.text"
          class="task-input"
          placeholder="Enter new task here"
          rows="5"
        ></textarea>


        <div class="options-row">
          <label class="important-option">
            <input type="checkbox" v-model="modalData.important" />
            <span>Important</span>
          </label>
          <input
            v-model="modalData.deadline"
            type="date"
            class="date-input"
          />
        </div>


        <div class="modal-actions">
          <button v-if="showEditModal" @click="deleteTask">
            Delete
          </button>
          <button @click="closeModal">Cancel</button>
          <button @click="confirmModal">OK</button>
        </div>
      </div>
    </div>

    <div v-if="showShareModal" class="modal-overlay">
      <div class="modal">
        <h2>Task Shared</h2>
        <p>You have successfully shared your task.</p>
        <p>
          The link is available in your profile or here:<br />
          <a :href="shareLink" target="_blank">{{ shareLink }}</a>
        </p>
        <div class="modal-actions">
          <button @click="closeShareModal">OK</button>
        </div>
      </div>
    </div>

  </div>
</template>

  
  <script>
  import api from '@/services/api';

  const TEACHER_ROLE = 1
  const STUDENT_ROLE = 2

  export default {
    name: 'TaskManager',
    data() {
      return {
        tasks: [],
        userId: null,
        showAddModal: false,
        showEditModal: false,
        showShareModal: false, 
        shareLink: '',
        shareError: '', 
        modalData: { id: null, text: '', deadline: '', important: false, completed: false },
        collapsedImportant: false,
        collapsedOthers: false,
        collapsedCompleted: false,
      };
    },
    computed: {
      importantTasks() {
        return this.tasks.filter(t => t.important && !t.completed);
      },
      otherTasks() {
        return this.tasks.filter(t => !t.important && !t.completed);
      },
      completedTasks() {
        return this.tasks.filter(t => t.completed);
      },
      groupedImportant() {
        return this.groupByDate(this.importantTasks);
      },
      groupedOthers() {
        return this.groupByDate(this.otherTasks);
      },
      groupedCompleted() {
        return this.groupByDate(this.completedTasks);
      }

    },
    methods: {
      async checkProfileComplete() {
        try {
          const userResp = await api.get('/users/get_me');
          if (userResp.status !== 200) throw new Error();
          const role = userResp.data.role;
          this.userId = userResp.data.id;

          if (role === STUDENT_ROLE) { 
            const stud = await api.get('/students/me');
          if (
            stud.status !== 200 ||
            !stud.data.full_name ||
            !stud.data.group_number
            ) {
            return this.$router.replace({ name: 'userPage' });
          }
          } else if (role === TEACHER_ROLE) { 
            const teach = await api.get('/teachers/me');
          if (teach.status !== 200 || !teach.data.FIO) {
            return this.$router.replace({ name: 'userPage' });
          }
          }
          return Promise.resolve();
        } catch {
          return this.$router.replace({ name: 'userPage' });
        }
      },
      async fetchTasks(){
        try {
          const response = await api.get('tasks/get_tasks_for_me');
          
          if (response.status !== 201) throw new Error(`Error ${response.status}`);
          
          this.tasks = response.data.map(task => ({
            id: task.task_id,
            text: task.description,
            deadline: task.deadline,
            important: Boolean(task.task_flag & 1),
            completed: Boolean(task.task_flag & 2),
          }));
      } catch (error) {
        console.error('Failed to fetch tasks:', error);
      }
    },
      async addTask(){
        try {
          const payload = {
            description: this.modalData.text,
            deadline: this.modalData.deadline
              ? new Date(this.modalData.deadline).toISOString()
              : null,
            task_flag: (this.modalData.important ? 1 : 0) | (this.modalData.completed ? 2 : 0)
          };
          const response = await api.post('tasks/create_task_for_me', payload);
          if (response.status === 201) {
            await this.fetchTasks();
          } else {
            console.error(`Create failed: ${response.status}`);
          }
      } catch (err) {
        console.error('Add task error', err);
      }
    },
      async updateTask(){
        try {
          const payload = {
            task_id: this.modalData.id,
            description: this.modalData.text,
            deadline: this.modalData.deadline
              ? new Date(this.modalData.deadline).toISOString()
              : null,
            task_flag: (this.modalData.important ? 1 : 0) | (this.modalData.completed ? 2 : 0)
          };
          const response = await api.patch('tasks/update_task', payload);
          if (response.status === 201) {
            await this.fetchTasks();
        } else {
            console.error(`Update failed: ${response.status}`);
          
        }
      } catch (err) {
        console.error('Update task error', err.response?.data || err);
      }
      },
      async deleteTask(){
        const response = await api.delete('tasks/delete_task', { data: { task_id: this.modalData.id } });
        if (response.status === 201){
          await this.fetchTasks();
        }
        else {
          throw new Error(`Error ${response.status}`);
        }
        this.closeModal();
      },
      async toggleComplete(task) {
        try {
          const newCompleted = !task.completed;
          
          const payload = {
            task_id: task.id,
            description: task.text,
            deadline: task.deadline
              ? new Date(task.deadline).toISOString()
              : null,
            task_flag: (task.important ? 1 : 0) | (newCompleted ? 2 : 0)
          };
          
          const response = await api.patch('tasks/update_task', payload);
          if (response.status === 201) {
            await this.fetchTasks();
          } else {
            console.error(`Toggle complete failed: ${response.status}`);
          }
        } catch (err) {
          console.error('Toggle complete error', err.response?.data || err);
        }
      },
      async shareTask(task) {
      try {
        const payload = {
          task_id: task.id,
          user_id: this.userId
        };
        const response = await api.post('/shared_links', payload);
        if (response.status === 201) {
          const token = response.data.token;
          this.shareLink = `http://185.95.159.198/api/shared_links/pretty/${token}`;
          this.shareError = '';
          this.showShareModal = true;
        } else {
          this.shareError = `Failed to share task (status ${status}).`;
          this.shareLink = '';
          this.showShareModal = true;
        }
      } catch (err) {
        console.error('Error sharing task:', err);
        this.shareError = 'An error occurred while sharing. Please try again later.';
        this.shareLink = '';
        this.showShareModal = true;
      }
    },
    closeShareModal() {
      this.showShareModal = false;
      this.shareLink = '';
      this.shareError = '';
    },
      

      groupByDate(list) {
        const noDeadline = list.filter(t => t.deadline === null);

        const withDeadline = list
          .filter(t => t.deadline !== null)
          .sort((a, b) => a.deadline.localeCompare(b.deadline));
        const acc = {};
        
        if (noDeadline.length) 
          acc[''] = noDeadline;
        
          withDeadline.forEach(t => {
          (acc[t.deadline] = acc[t.deadline] || []).push(t);
        });
        return acc;
      },
      openAddModal() {
        this.modalData = { id: null, text: '', deadline: '', important: false, completed: false };
        this.showAddModal = true;
      },
      openEditModal(task) {
        this.modalData = { ...task };
        this.showEditModal = true;
      },
      closeModal() {
        this.showAddModal = this.showEditModal = this.showDeleteConfirm = false;
        this.modalData = { id: null, text: '', deadline: '', important: false, completed: false };
      },
      confirmModal() {
        if (this.showAddModal) {
          this.addTask();
        
        } else if (this.showEditModal) {
          this.updateTask();
        }
        this.closeModal();
      },
      formatDate(dateStr) {
        const d = new Date(dateStr);
        const dd = String(d.getDate()).padStart(2, '0');
        const mm = String(d.getMonth() + 1).padStart(2, '0');
        const yyyy = d.getFullYear();
        return `${dd}-${mm}-${yyyy}`;
      },
      isUrgent(task) {
        if (!task.deadline || task.completed) return false;

        const deadline = new Date(task.deadline);
        const today = new Date();
        const diffInDays = Math.floor((deadline - today) / (1000 * 60 * 60 * 24));

        return diffInDays < 0 || diffInDays <= 3;
      }
    },
    created() {
      this.checkProfileComplete()
      .then(() => this.fetchTasks());
    },
  };
  </script>
  


  <style scoped>
  .task-manager {
    position: relative;
    height: 100vh;
    overflow: hidden;

    min-width: 700px;
    overflow-x: auto;
  }
  .content {
    height: 100%;
    overflow-y: auto;
    /* background-color: #e0e0e0; */
    /* background-color: #d0dfeb; */
    background-color: #d9e2eb;
    padding: 16px 56px 16px;
  }

  ul {
    list-style: none;
    margin: 0;
    padding: 0;
  }

  .blurred {
    filter: blur(4px);
  }
  .section {
    margin-bottom: 24px;
  }

  .section header {
    display: flex;
    align-items: center;
    justify-content: center;    
    position: relative;        
    cursor: pointer;
    background: #79b9f5;
    padding: 8px;
    border-radius: 4px;

    /* height: 48px;      
    box-sizing: border-box; */
  }


  .toggle-icon {
    display: inline-block; 
    transition: transform 0.5s ease; 
    font-size: 1.2em;
    line-height: 1em;
    width: 1em;
    height: 1em;
    text-align: center;                
  }

  .toggle-icon.rotated {
    transform: rotate(90deg);
  }

  .collapse-enter-active,
  .collapse-leave-active {
    transition: max-height 0.5s ease, opacity 0.5s ease;
    overflow: hidden;
  }

  .collapse-enter-from,
  .collapse-leave-to {
    max-height: 0;
    opacity: 0;
  }

  .collapse-enter-to,
  .collapse-leave-from {
    max-height: 1000px;
    opacity: 1;
  }


  .section header h2 {
    text-align: center;
  }

  .section header span {
    position: absolute;         
    right: 12px;
  }
  .section-content {
    margin-top: 8px;
    margin-bottom: 8px;
  }
  .section-content h3 {
    margin: 12px 0 4px;

  }
  .task-item {
    display: flex;
    align-items: center;
    justify-content: flex-start; 

    background-color: #f5f5f5;
    border-radius: 8px;
    padding: 4px 8px;
    margin-bottom: 8px;

    transition: background-color 0.2s ease;
  }
  .task-item:hover {
    background-color: #2525250d;
  }

  .task-text {
    flex: 1;          
    margin-left: 8px;
    text-align: left;  
    word-break: break-word;
  }

  .more-actions {
    visibility: hidden;
  }

  .task-item:hover .more-actions {
    visibility: visible;
  }

  .more-actions button {
    background: transparent;
    border: none;
    font-size: 18px;
    cursor: pointer;
    padding: 4px;
  }

  .more-actions {
  display: flex;
  gap: 4px;
  visibility: hidden;
}
.task-item:hover .more-actions {
  visibility: visible;
}
.share-btn {
  background: transparent;
  border: none;
  cursor: pointer;
  font-size: 18px;      
  padding: 4px;
}

  .task-item:hover {
    background-color: rgba(0,0,0,0.05);
  }

  .task-item.completed .task-text {
    color: #888;
    text-decoration: line-through;
  }
  .actions {
    visibility: hidden;
  }
  .task-item:hover .actions {
    visibility: visible;
  }
  .add-btn {
    /* position: fixed; */
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
    box-shadow: 0 2px 8px rgba(0,0,0,0.2);
  }

  .modal {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);


  width: 60%;
  min-width: 320px;
  max-width: 90%;
  
  padding: 24px; 
  box-sizing: border-box; 
  /* background: #b8d9ff; */
  background: #ffffff;
  border-radius: 8px;
  box-shadow: 0 4px 12px rgba(0,0,0,0.15);
  
}

/* .modal-overlay {
  position: absolute;    
  top: 0; left: 0;
  width: 100%; height: 100%;
  background: rgba(143, 143, 143, 0.5);  
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;        
} */


.modal-title {
  margin: 0 0 16px;
  text-align: center;
}

.task-input {
  width: 100%;
  padding: 8px 12px;
  font-size: 16px;
  /* border: 1px solid #ccc; */
  border-radius: 4px;
  box-sizing: border-box;  
  margin-bottom: 16px;

  resize: vertical;
  height: auto;
  min-height: calc(1.2em * 5 + 16px); 
  max-height: 200px;
  overflow-y: auto;

  /* background: #ffffff; */
  background: #f5f5f5;
  border: 1px solid #ddd
}

.options-row {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 24px;
}

.important-option {
  display: flex;
  align-items: center;
  cursor: pointer;
}
.important-option span {
  margin-left: 8px;
  font-size: 14px;
}

.date-input {
  padding: 6px 8px;
  font-size: 14px;
  /* border: 1px solid #ccc; */
  border-radius: 4px;
  cursor: pointer;
  background: #f5f5f5;
  border: 1px solid #ddd
}

.task-input:focus,
.date-input:focus {
  outline: none;                                    
  box-shadow: 0 0 0 1.5px rgba(134, 134, 134, 0.6);   
  border-color: #a0a0a0;                            
}

.modal-actions {
  display: flex;
  justify-content: flex-end;
  gap: 8px;
}

.modal button {
  background: #46637f;
  color: #ffffff;
  border: none;
  cursor: pointer;
  border-radius: 10%;
  font-size: 14px;
  /* width: 40px; */
  height: 40px;
  box-shadow: 0 2px 4px rgba(0,0,0,0.2);
}


.task-item.urgent:not(.completed) {
  background-color: #ffe5e5;
}


</style>
  