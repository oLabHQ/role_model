<template>
  <ul class="list-unstyled components">
    <slot/>
  </ul>
</template>

<script>
export default {
}
</script>

<style scoped>
ul {
    min-width: 250px;
    max-width: 250px;
    background: #7386D5;
    color: #fff;
    transition: all 0.3s;
    padding: 20px 0;
    padding-bottom: 0px;
}
</style>
