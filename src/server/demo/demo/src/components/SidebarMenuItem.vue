<template>
  <li>
    <a href="#">
      <i></i>
      <slot></slot>
    </a>
  </li>
</template>

<script>
export default {
}
</script>

<style scoped>
a {
    padding: 10px;
    font-size: 1.1em;
    display: block;
    text-align: left;
}

a:hover {
    color: #7386D5;
    background: #fff;
}

a,
a:hover,
a:focus {
    color: inherit;
    text-decoration: none;
    transition: all 0.3s;
}

i {
    margin-right: 10px;
}
</style>
