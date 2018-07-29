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
