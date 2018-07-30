<template>
  <div>
    <Sidebar
      heading="Acme Ltd">
      <SidebarMenu v-if="displayEvents.length > 0">
        <SidebarMenuItem  v-if="appliedEvents.length > 0" href="#">
          {{ currentDate }}
        </SidebarMenuItem>
        <SidebarMenuItem  v-else href="#">
          Move the slider <span style="float: right">⬇</span>
        </SidebarMenuItem>
        <SidebarMenuItem href="#">
          Event: {{ cursor }} of {{ (displayEvents || []).length }}
          <br/>
          <input
            type="range"
            v-model="cursor"
            min="0"
            :max="displayEvents.length"/>
        </SidebarMenuItem>
        <SidebarMenuItem
          href="http://google.com">Organization Chart</SidebarMenuItem>
        <SidebarSubmenu name="Roles">
          <SidebarSubmenuItem
            href="#"
            v-bind:key="role.pk"
            v-for="role in displayedRoles">{{ role.fields.name }}
          </SidebarSubmenuItem>
        </SidebarSubmenu>
        <SidebarSubmenu name="Events">
          <SidebarSubmenuItem
            v-bind:key="e.pk"
            v-for="e in appliedEvents.slice().reverse()"
            href="#">{{ e.event }} {{ e.instance.model.split(".")[1] }} on {{ e.created | formatDate }}</SidebarSubmenuItem>
        </SidebarSubmenu>
      </SidebarMenu>
    </Sidebar>
    <div id="content">
      {{ currentIndex }}
      {{ appliedEvents.length }}
    </div>
  </div>
</template>

<script>
import gql from 'graphql-tag'
import moment from 'moment'

import Sidebar from './Sidebar.vue'
import SidebarMenu from './SidebarMenu.vue'
import SidebarSubmenu from './SidebarSubmenu.vue'
import SidebarMenuItem from './SidebarMenuItem.vue'
import SidebarSubmenuItem from './SidebarSubmenuItem.vue'

export default {
  name: 'Graph',
  props: {

  },
  components: {
    Sidebar,
    SidebarMenu,
    SidebarSubmenu,
    SidebarMenuItem,
    SidebarSubmenuItem
  },
  apollo: {
    organizationEvents: gql`{
      organizationEvents {
        pk
        event
        created
        serializedChanges
        changes @client
        serializedInstance {
          pk
          model
          fields
        }
        instance @client
      }
    }`
  },
  methods: {
    pushEvent (e) {
      this.appliedEvents.push(e)
      if (e.event === 'created') {
        var instance = Object.assign({}, e.instance);
        instance.fields = Object.assign({}, e.instance.fields)
        this.$set(this.data, e.instance.pk, instance)
        if (e.instance.model === 'role_model.role') {
          this.roles.push(instance.pk)
        }
      }
      if (e.event === 'modified') {
        for (var field in e.changes) {
          if (e.changes.hasOwnProperty(field)) {
            const change = e.changes[field]
            const valueTo = change[0]
            this.data[e.instance.pk].fields[field] = valueTo
          }
        }
      }
    },
    popEvent () {
      var e = this.appliedEvents.pop()
      if (e.event === 'created') {
        delete this.data[e.pk]
        if (e.instance.model === 'role_model.role') {
          this.roles.pop()
        }
      }
      if (e.event === 'modified') {
        for (var field in e.changes) {
          if (e.changes.hasOwnProperty(field)) {
            const change = e.changes[field]
            const valueFrom = change[1]
            this.data[e.instance.pk].fields[field] = valueFrom
            console.log("Set valueFrom")
          }
        }
      }
    },
    applyDelta (delta) {
      if (delta > 0) {
        const nextIndex = this.nextIndex
        for (var i = this.appliedEvents.length;
          i <= nextIndex; i++) {
          this.pushEvent(this.organizationEvents[i])
        }
      } else if (delta < 0) {
        const previousIndex = this.previousIndex
        for (var j = this.appliedEvents.length;
          j > (previousIndex || -1) + 1; j--) {
          this.popEvent()
        }
      }
    }
  },
  watch: {
    cursor (value) {
      const delta = value - this.previousCursor
      if (delta !== 0) {
        this.applyDelta(delta)
      }
      this.previousCursor = value
    }
  },
  computed: {
    displayedRoles() {
      return (this.roles.map((pk) => this.data[pk])
        .filter((role) => !role.fields.is_deleted))
    },
    eventsIndex () {
      const eventsIndexObject = {}
      this.organizationEvents.forEach((e, index) => {
        eventsIndexObject[e.pk] = index
      })
      return eventsIndexObject
    },
    displayEvents () {
      return (this.organizationEvents || []).filter((e, index) => {
        const isDisplayed = [
          'role_model.group',
          'role_model.role',
          'role_model.assignment'
        ].indexOf(e.instance.model) !== -1
        return isDisplayed
      })
    },
    nextIndex () {
      if (this.currentEvent) {
        return this.eventsIndex[this.currentEvent.pk]
      }
    },
    previousIndex () {
      if (this.previousEvent) {
        return this.eventsIndex[this.previousEvent.pk]
      }
    },
    previousEvent () {
      if (this.cursor < 1) {
        return null
      }
      return this.displayEvents[this.cursor - 1]
    },
    currentEvent () {
      if (this.cursor === 0) {
        return null
      }
      return this.displayEvents[this.cursor - 1]
    },
    currentDate () {
      if (this.currentEvent) {
        return (moment(this.currentEvent.created)
          .format('Do MMMM YYYY'))
      }
    }
  },
  data () {
    return {
      data: {},
      roles: [],
      appliedEvents: [],
      previousCursor: 0,
      currentIndex: 0,
      organizationEvents: [],
      date: '1990-12-12',
      cursor: 0
    }
  }
}
</script>

<style scoped>
input {
  width: 100%;
}

div {
  display: flex;
  align-items: stretch;
}

#content {
    width: 100%;
    padding: 20px;
    min-height: 100vh;
    transition: all 0.3s;
}
</style>
