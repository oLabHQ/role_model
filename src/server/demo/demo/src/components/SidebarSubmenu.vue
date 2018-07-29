<template>
  <li>
    <a
        href="#"
        aria-expanded="false"
        class="dropdown-toggle"
        v-b-toggle="submenuId">
      <i></i>
      {{ name }}
    </a>
    <b-collapse :id="submenuId">
      <ul class="list-unstyled">
          <slot></slot>
      </ul>
    </b-collapse>
  </li>
</template>

<script>
const uuidv4 = require('uuid/v4')

export default {
  props: {
    name: {
      type: String,
      default: ''
    }
  },
  data () {
    return {
      submenuId: 'submenu-' + uuidv4()
    }
  }
}
</script>

<style scoped>
a {
    padding: 10px;
    font-size: 1.1em;
    display: block;
    position: relative;
    text-align: left;
}

a:hover {
    color: #7386D5;
    background: #fff;
    text-decoration: none;
    transition: all 0.3s;
}

i {
    margin-right: 10px;
}

li.active > a,
a[aria-expanded="true"] {
    color: #fff;
    background: #6d7fcc;
}

a,
a:focus {
    color: inherit;
}

a::after {
    display: block;
    position: absolute;
    top: 50%;
    right: 20px;
    transform: translateY(-50%);
}

</style>
