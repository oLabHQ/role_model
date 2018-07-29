<template>
  <li>
    <a
        href="#"
        aria-expanded="false"
        class="dropdown-toggle"
        v-b-toggle="submenuId">
      <i></i>
      Home
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
  data () {
    return {
      submenuId: 'submenu-' + uuidv4()
    }
  }
  // mounted () {
  //   this.submenuId = uuidv4()
  // }
  // props: {
  //   _submenuId: {
  //     type: String,
  //     default: ''
  //   }
  // },
  // computed: {
  //   submenuId () {
  //     return this._submenuId
  //   }
  // }
}
// SidebarItem._submenuId = uuidv4()
// console.log(SidebarItem._submenuId)
</script>

<style scoped>
ul.list-unstyled {
    padding: 20px 0;
    border-bottom: 1px dotted #47748b;
}

ul li a {
    padding: 10px;
    font-size: 1.1em;
    display: block;
}

ul li a:hover {
    color: #7386D5;
    background: #fff;
}

ul li a i {
    margin-right: 10px;
}

ul li.active>a,
a[aria-expanded="true"] {
    color: #fff;
    background: #6d7fcc;
}

a,
a:hover,
a:focus {
    color: inherit;
    text-decoration: none;
    transition: all 0.3s;
}
li a {
    text-align: left;
}
.dropdown-toggle {
    position: relative;
}

.dropdown-toggle::after {
    display: block;
    position: absolute;
    top: 50%;
    right: 20px;
    transform: translateY(-50%);
}

li ul a {
    font-size: 0.9em !important;
    padding-left: 30px !important;
    background: #6d7fcc;
}
</style>
