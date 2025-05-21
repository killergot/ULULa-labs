<template>
  <div class="sidebar" :class="{ collapsed }">

    <button @click="$emit('toggle')" class="toggle-btn">
      <span v-if="!collapsed">❮</span>
      <span v-else>❯</span>
    </button>


    <div v-show="!collapsed" class="sidebar-content">
      <nav class="menu">
        <ul>
          <li v-for="item in pages" :key="item.name">
            <router-link :to="item.link">{{ item.name }}</router-link>
          </li>
        </ul>
      </nav>

      <hr class="divider">

      <div class="folders-section">
        <ul>
          <li v-for="item in folders" :key="item.name" class="folder-item">
            <span class="folder-icon">📁</span>
            <span class="folder-name">{{ item.name }}</span>
          </li>
        </ul>
        <button @click="addFolder" class="add-folder-btn">+ folder</button>
      </div>
    </div>


    <button
      v-show="!collapsed"
      @click="logout"
      class="logout-btn"
    >
      Logout
    </button>
  </div>
</template>

<script>
import { clearTokens, getRefreshToken } from '@/utils/token';
import api from '@/services/api';

export default {
  name: 'SidebarMenu',
  props: {
    collapsed: { type: Boolean, default: false }
  },
  data() {
    return {
      pages: [
        { name: 'Home', link: '/' },
        { name: 'My profile', link: '/userPage' }
      ],
      folders: [
        { name: 'Личные' },
        { name: 'Рабочие' }
      ],
      counter: 1
    };
  },
  methods: {
    addFolder() {
      this.folders.push({ name: `Новая папка ${this.counter++}` });
    },
    async logout() {
      try {
        const refreshToken = getRefreshToken();
        if (refreshToken) {
          const { data: sessions } = await api.get('/users/my_sessions');
          const current = sessions.find(s => s.token === refreshToken);
          if (current) await api.delete(`/users/my_sessions/${current.id}`);
        }
      } catch (err) {
        console.error('Logout failed:', err);
      } finally {
        clearTokens();
        this.$router.push('/login');
      }
    }
  }
};
</script>

<style scoped>
.sidebar {
  position: fixed;
  top: 0; bottom: 0; left: 0;
  width: 200px;
  background: #34495e;
  color: #fff;

  display: flex;
  flex-direction: column;
  justify-content: space-between;

  padding: 3rem 0.6rem 1rem;
  transition: width 0.3s ease;
  z-index: 1000;
}
.sidebar.collapsed {
  width: 50px;
}

.toggle-btn {
  background: none;
  border: none;
  color: inherit;
  font-size: 1.2rem;
  padding: 1rem;
  cursor: pointer;
}

.sidebar-content {
  flex: 1 1 auto;
  overflow-y: auto;
}

.menu {
  margin-top: 1rem;
}
.menu ul { list-style: none; padding: 0; }
.menu li { margin: 0.8rem 0; }
.menu a { color: inherit; text-decoration: none; font-size: 1.05rem; line-height: 1.4;}

.divider {
  border: 0;
  border-top: 1px solid #46637f;
  margin: 1rem 0;
}

.folders-section { padding: 0 0.5rem; }
.folder-item {
  display: flex;
  align-items: center;
  margin: 0.5rem 0;
  padding: 0.5rem;
  border-radius: 4px;
  transition: background 0.2s;
}
.folder-item:hover { background: #40576b; }
.folder-icon { margin-right: 0.5rem; }
.folder-name {   font-size: 1.05rem; }

.add-folder-btn {
  width: 100%;
  padding: 0.5rem;
  margin-top: 0.5rem;
  background: #46637f;
  color: #fff;
  border: none;
  border-radius: 4px;
  font-size: 1.05rem;
  cursor: pointer;
  transition: background 0.2s;
}
.add-folder-btn:hover { background: #567892; }

.logout-btn {
  align-self: stretch;
  padding: 0.75rem 1rem;
  font-size: 1.05rem;
  background: #46637f;
  color: #fff;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  transition: background 0.2s;
}
.logout-btn:hover { background: #567892; }
</style>
