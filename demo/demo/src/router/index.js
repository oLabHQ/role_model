import Vue from 'vue'
import Router from 'vue-router'
import Index from '@/components/Index'

import 'bootstrap/dist/css/bootstrap.css'
import 'bootstrap-vue/dist/bootstrap-vue.css'
import 'vue-cytoscape/dist/vue-cytoscape.css'
import 'es7-object-polyfill'

Vue.use(Router)

export default new Router({
  routes: [
    {
      path: '/',
      name: 'Index',
      component: Index
    }
  ]
})
