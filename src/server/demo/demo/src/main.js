// The Vue build version to load with the `import` command
// (runtime-only or standalone) has been set in webpack.base.conf with an alias.
import Vue from 'vue'
import Cookies from 'js-cookie'
import BootstrapVue from 'bootstrap-vue'
import App from './App'
import router from './router'
import moment from 'moment'
import { ApolloClient } from 'apollo-client'
import { ApolloLink } from 'apollo-link'
import { HttpLink } from 'apollo-link-http'
import { withClientState } from 'apollo-link-state'
import { setContext } from 'apollo-link-context'
import { InMemoryCache } from 'apollo-cache-inmemory'
import VueApollo from 'vue-apollo'

const httpLink = new HttpLink({
  uri: 'http://localhost:8000/demo/graphql',
  credentials: 'include'
})

const authLink = setContext((_, { headers }) => {
  const csrfToken = Cookies.get('csrftoken')
  return {
    headers: {
      ...headers,
      'X-CSRFToken': csrfToken || ''
    }
  }
})

var cache = new InMemoryCache()

const linkStateResolvers = {
  History: {
    changes: (history, args, ctx) => {
      const serializedChanges = history.serializedChanges
      if (serializedChanges) {
        return JSON.parse(serializedChanges)
      }
      return null
    },
    instance: (history, args, ctx) => {
      const serializedInstance = history.serializedInstance
      if (serializedInstance) {
        return {
          pk: serializedInstance.pk,
          model: serializedInstance.model,
          fields: JSON.parse(serializedInstance.fields)
        }
      }
      return null
    }
  }
}

const stateLink = withClientState({
  cache: cache,
  resolvers: linkStateResolvers
})

const apolloClient = new ApolloClient({
  link: ApolloLink.from([stateLink, authLink, httpLink]),
  cache: cache,
  connectToDevTools: true
})

const apolloProvider = new VueApollo({
  defaultClient: apolloClient
})

Vue.use(VueApollo)
Vue.use(BootstrapVue)

Vue.filter('formatDate', function (value) {
  if (value) {
    return moment(String(value)).format('Do MMMM')
  }
})

Vue.config.productionTip = false

/* eslint-disable no-new */
new Vue({
  el: '#app',
  provide: apolloProvider.provide(),
  router,
  components: { App },
  template: '<App/>'
})
