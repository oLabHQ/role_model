<template>
  <li>
    <a :href="href">
      <i></i>
      <slot></slot>
    </a>
  </li>
</template>

<script>
export default {
  props: {
    href: {
      default: false
    }
  }
}
</script>

<style scoped>
li {
  cursor: default;
}
a {
    padding: 10px;
    font-size: 1.1em;
    display: block;
    text-align: left;
}

a:hover {
    color: #7386D5 !important;
    background: #fff;
    text-decoration: none;
    transition: all 0.3s;
}

a,
a:focus {
    color: inherit;
    text-decoration: none;
    transition: all 0.3s;
}

i {
    margin-right: 10px;
}
</style>
