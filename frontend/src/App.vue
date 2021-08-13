<template>
  <Nav />
  <router-view/>
  <Footer />
</template>

<style>
@import "assets/css/bootstrap.css";
@import "assets/css/font-awesome.css";
@import "assets/css/style.css";
</style>
<script>
import Nav from "./components/Nav";
import Footer from "./components/Footer";
export default {
  components: {
    Nav,
    Footer,
  }
}
</script>