<template>
  <div class="hello">
    <h1>{{ msg }}</h1>
    <h3 class="lionhu">by Lionhu</h3>



  </div>
</template>

<script>

export default {
  name: 'HelloWorld',
  props: {
    msg: String
  },
      data() {
      return {
        };
    },
  components:{
  },
  methods: {

    }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style lang="scss" scoped>
  @import "src/assets/scss/colors";
h3 {
  margin: 40px 0 0;
}
ul {
  list-style-type: none;
  padding: 0;
}
li {
  display: inline-block;
  margin: 0 10px;
}
a {
  color: $danger;
}

</style>
