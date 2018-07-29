<template>
  <li>
    <a href="#">
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
    font-size: 0.9em !important;
    padding-left: 30px !important;
    background: #6d7fcc;
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

li.active > a {
    color: #fff;
    background: #6d7fcc;
}
</style>
