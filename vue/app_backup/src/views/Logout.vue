<template>
  <div >
    <Navbar></Navbar>
    <div class="container text-dark">
      <div class="row justify-content-md-center">
        <div class="col-md-5 p-3 login justify-content-md-center">
          <h1 class="h3 mb-3 font-weight-normail text-center">Please Sign in</h1>

          <p>Wrong creditial information, try again. </p>

          <form >
            <div class="form-group">
              <input type="text" name="username" id="user" v-model="username">
            </div>
            <div class="form-group">
              <input type="text" name="password" id="pass" v-model="password">
            </div>
            <button type="submit" class="btn btn-lg btn-primary btn-block">Login</button>
          </form>

        </div>
      </div>
    </div>
  </div>
</template>

<script>
    // import { getAPI } from '../axios-api'
import Navbar    from "../components/Navbar.vue";
export default {
  name: 'Login',
    data () {
      return {
          APIData: [],
        username:"",
        password:"",
        }
    },
  components:{
      Navbar
  },
    created () {
      console.log("login")
        // getAPI.get('/expenses/',)
        //   .then(response => {
        //     console.log('Post API has recieved data')
        //     this.APIData = response.data
        //   })
        //   .catch(err => {
        //     console.log(err)
        //   })
    }
}
</script>

<style>

</style>
