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
      <cytoscape :config="config"/>
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
    pushNode (cy, node) {
      this.elements.push(cy.add({
        data: node
      }))
    },
    popNode (cy) {
      cy.remove(this.elements.pop())
    },
    runLayout (cy) {
      cy.layout(this.layout).run()
    },
    pushEvent (e) {
      this.appliedEvents.push(e)
      if (e.event === 'created') {
        var instance = Object.assign({}, e.instance)
        instance.fields = Object.assign({}, e.instance.fields)
        this.$set(this.data, e.instance.pk, instance)

        this.$cytoscape.instance.then(cy => {
          var node
          var color
          switch (e.instance.model) {
            case 'role_model.role':
              color = this.group_colors[instance.fields.group]
              node = {
                id: instance.pk,
                name: instance.fields.name,
                width: instance.fields.name.length * 16,
                parent: instance.fields.group,
                color: color
              }
              this.pushNode(cy, node)
              break
            case 'role_model.group':
              color = this.nextColor
              this.$set(this.group_colors, instance.pk, color)
              node = {
                id: instance.pk,
                name: instance.fields.name,
                width: instance.fields.name.length * 16,
                color: color
              }
              this.pushNode(cy, node)
              break
          }
          this.runLayout(cy)
        })
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
        if (e.instance.model === 'role_model.role' ||
            e.instance.model === 'role_model.group') {
          this.roles.pop()
          this.$cytoscape.instance.then(cy => {
            this.popNode(cy)
            this.runLayout(cy)
          })
        }
      }
      if (e.event === 'modified') {
        for (var field in e.changes) {
          if (e.changes.hasOwnProperty(field)) {
            const change = e.changes[field]
            const valueFrom = change[1]
            this.data[e.instance.pk].fields[field] = valueFrom
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
    nextColor () {
      const colorIndex = (Object.keys(this.group_colors).length %
        this.colors.length)
      return this.colors[colorIndex]
    },
    displayedRoles () {
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
      layout: {
        name: 'circle',
        padding: 20
      },
      data: {},
      roles: [],
      group_colors: {},
      elements: [],
      appliedEvents: [],
      previousCursor: 0,
      currentIndex: 0,
      organizationEvents: [],
      cursor: 0,
      colors: [
        '#6FB1FC',
        '#EDA1ED',
        '#86B342',
        '#F5A45D',
        '#6456B7',
        '#FF007C'
      ],
      config: {
        elements: {
          nodes: [],
          edges: []
        },
        layout: {
          name: 'cose',
          padding: 20
        },
        style: [
          {
            selector: 'node[width]',
            css: {
              width: 'data(width)'
            }
          },
          {
            selector: 'node[color]',
            css: {
              'text-outline-color': 'data(color)',
              'background-color': 'data(color)'
            }
          },
          {
            selector: 'node',
            css: {
              'shape': 'roundrectangle',
              'padding': '5',
              'content': 'data(name)',
              'text-valign': 'center',
              'text-outline-width': 2,
              'color': '#fff',
              'font-size': 24,
              'font-family': 'monaco'
            }
          },
          {
            selector: '$node > node',
            css: {
              // 'text-outline-color': 'data(color)',
              'text-outline-width': 4,
              'padding-top': '10px',
              'padding-left': '10px',
              'padding-bottom': '10px',
              'padding-right': '10px',
              'text-valign': 'top',
              'text-halign': 'center',
              // 'background-color': 'data(color)',
              'background-opacity': '0.1',
              'font-size': 24
            }
          },
          {
            selector: 'edge',
            css: {
              // 'content': 'data(name)',
              'target-arrow-shape': 'triangle',
              'control-point-step-size': '150px',
              'curve-style': 'bezier',
              'opacity': 0.9,
              'width': '5',
              'arrow-scale': 2.5,
              // 'source-arrow-shape': 'circle',
              // 'line-color': 'data(line_color)',
              'color': 'white',
              'text-outline-width': '3',
              'text-outline-color': 'black',
              'font-size': '24',
              // 'source-arrow-color': 'data(source_color)',
              // 'target-arrow-color': 'data(source_color)',
              'edge-text-rotation': 'autorotate'
            }
          },
          {
            selector: ':selected',
            css: {
              'background-color': 'black',
              'line-color': 'black',
              'target-arrow-color': 'black',
              'source-arrow-color': 'black'
            }
          }
        ]
      }
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
