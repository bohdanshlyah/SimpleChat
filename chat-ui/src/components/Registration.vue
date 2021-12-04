<template>
  <div>
    <input v-model="login" placeholder="Login" type="text"/>
    <input v-model="password" placeholder="Password" type="password"/>
    <button @click="setRegistration">Sing IN</button>
  </div>
</template>

<script>
import $ from 'jquery'
export default {
  name: 'Registration',
  data () {
    return {
      login: '',
      password: ''
    }
  },
  methods: {
    setRegistration () {
      $.ajax({
        url: 'http://localhost:8000/auth/users/',
        type: 'POST',
        data: {
          username: this.login,
          password: this.password
        },
        success: (response) => {
          alert('Registration success! And now You can Login.')
          this.$router.push({name: 'home'})
        },
        error: (response) => {
          alert('Username alredy exist or the password is too similar to the username.')
        }
      })
    }
  }
}
</script>
