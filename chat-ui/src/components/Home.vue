<template v-slot:home>
  <div>
    <h1>CHAT</h1>
    <div>
      {{env}}
    </div>
    <button v-if="!auth" @click="goReg">Sing IN</button>
    <button v-if="!auth" @click="goLogin">Login</button>
    <button v-else @click="logout">Logout</button>

    <Chat v-if="auth" @openDialog='openDialog'></Chat>
    <Dialog v-if="dialog.show" :id='dialog.id'></Dialog>
  </div>
</template>

<script>
import Chat from '@/components/Chat.vue'
import Dialog from '@/components/Dialog.vue'
export default {
  name: 'Home',
  components: {
    Chat,
    Dialog
  },
  props: {id: ''},
  data () {
    return {
      dialog: {
        id: '',
        show: false
      },
      form: {
        textarea: ''
      },
      env: process.env.baseUrl
    }
  },
  computed: {
    auth () {
      if (sessionStorage.getItem('auth_token')) {
        return true
      }
    }
  },
  methods: {
    goReg () {
      this.$router.push({name: 'registration'})
    },
    goLogin () {
      this.$router.push({name: 'login'})
    },
    logout () {
      sessionStorage.removeItem('auth_token')
      window.location = '/'
    },
    openDialog (id) {
      this.dialog.id = id
      this.dialog.show = true
    }
  }
}
</script>
