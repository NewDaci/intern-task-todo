<script>
import Navbar from './components/Navbar.vue'

export default {
  components: {
    Navbar,
  },
};
</script>

<template>
  <Navbar />
  <div>
    <RouterView />
</div>
</template>

<style>
/* Add your global styles here */
</style>