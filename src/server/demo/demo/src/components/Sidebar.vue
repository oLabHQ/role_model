<template>
  <nav>
      <div>
          <h3>{{ heading }}</h3>
          <strong>{{ headingShort }}</strong>
      </div>
      <slot></slot>

  </nav>
</template>

<script>
export default {
  props: {
    heading: {
      type: String,
      default: ''
    },
    headingShort: {
      type: String,
      default: ''
    }
  }
}
</script>

<style scoped>
ul.CTAs {
    padding: 20px;
}

ul.CTAs a {
    text-align: center;
    font-size: 0.9em !important;
    display: block;
    border-radius: 5px;
    margin-bottom: 5px;
}
nav {
    min-width: 250px;
    max-width: 250px;
    background: #7386D5;
    color: #fff;
    transition: all 0.3s;
}

div {
    padding: 20px;
    background: #6d7fcc;
}

strong {
    display: none;
    font-size: 1.8em;
}
</style>
