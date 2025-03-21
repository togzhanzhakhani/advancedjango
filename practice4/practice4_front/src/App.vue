<template>
  <v-app>
    <v-container>
      <h1>Welcome to My Vue App</h1>
      
      <nav>
        <router-link to="/">Login</router-link> |
        <router-link to="/register">Register</router-link> |
        <router-link to="/admin" v-if="isAdmin">Admin Panel</router-link>
      </nav>

      <router-view></router-view>
    </v-container>
  </v-app>
</template>

<script>
import apiService from '@/services/apiService';

export default {
  data() {
    return {
      user: apiService.getUser()
    };
  },
  computed: {
    isAdmin() {
      return this.user && this.user.role === 'admin';
    }
  }
};
</script>

<style scoped>
v-app {
  background-color: #f4f4f9;
  min-height: 100vh;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
}

.v-container {
  text-align: center;
  max-width: 600px;
  padding: 20px;
}

h1 {
  font-size: 28px;
  color: #333;
  margin-bottom: 20px;
}

nav {
  margin-bottom: 20px;
  background: #8668b0;
  padding: 10px;
  border-radius: 5px;
}

nav a {
  color: white;
  text-decoration: none;
  font-weight: bold;
  margin: 0 10px;
  transition: color 0.3s ease-in-out;
}

nav a:hover {
  color: #ffeb3b;
}

.router-link-active {
  text-decoration: underline;
}
</style>