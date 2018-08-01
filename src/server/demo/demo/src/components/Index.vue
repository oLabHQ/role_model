<template>
  <div>
    <Sidebar
      heading="Awesome Startup">
      <SidebarMenu v-if="displayEvents.length > 0">
        <SidebarMenuItem  v-if="appliedEvents.length > 0">
          {{ currentDate }}
        </SidebarMenuItem>
        <SidebarMenuItem  v-else style="background: #FF5470">
          Start your journey <span style="float: right">⬇</span>
        </SidebarMenuItem>
        <SidebarMenuItem>
          Event: {{ cursor }} of {{ (displayEvents || []).length }}
          <br/>
          <input
            type="range"
            v-model="cursor"
            min="0"
            :max="displayEvents.length"/>
        </SidebarMenuItem>
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
    <div id="contact"
        v-if="cursor == (displayEvents || []).length && cursor > 0">
      <div class="block">
        <h2><a href="mailto:hn@olab.com.au">hn@olab.com.au</a></h2>
      </div>
    </div>
    <div id="content">
      <cytoscape
        :config="config"/>
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
    getElement (cy, nodeId) {
      return cy.getElementById(nodeId)
    },
    toggleElement (cy, nodeId, isHidden) {
      const elements = this.getElement(cy, nodeId)
      if (isHidden) {
        elements.hide()
      } else {
        elements.show()
      }
    },
    pushNode (cy, data) {
      this.elements.push(cy.add({
        data: data
      }))
    },
    popNode (cy) {
      cy.remove(this.elements.pop())
    },
    runLayout (cy) {
      cy.layout(this.layout).run()
    },
    inputTypes (responsibility) {
      var responsibilities = this.responsibilityInputTypes[responsibility] || {}
      return Object.keys(responsibilities).map((pk) => responsibilities[pk])
    },
    roleColor (role) {
      return this.group_colors[role.fields.group]
    },
    incrementRoleInputType (role, contentType) {
      if (!this.edgeMeta.rolesWithInputType[contentType.pk]) {
        this.$set(this.edgeMeta.rolesWithInputType, contentType.pk, {})
      }
      if (!this.edgeMeta.rolesWithInputType[contentType.pk][role.pk]) {
        this.$set(this.edgeMeta.rolesWithInputType[contentType.pk], role.pk, 0)
      }
      this.edgeMeta.rolesWithInputType[contentType.pk][role.pk]++
    },
    decrementRoleInputType (role, contentType) {
      this.edgeMeta.rolesWithInputType[contentType.pk][role.pk]--
    },
    incrementRoleOutputType (role, contentType) {
      if (!this.edgeMeta.rolesWithOutputType[contentType.pk]) {
        this.$set(this.edgeMeta.rolesWithOutputType, contentType.pk, {})
      }
      if (!this.edgeMeta.rolesWithOutputType[contentType.pk][role.pk]) {
        this.$set(this.edgeMeta.rolesWithOutputType[contentType.pk], role.pk, 0)
      }
      this.edgeMeta.rolesWithOutputType[contentType.pk][role.pk]++
    },
    decrementRoleOutputType (role, contentType) {
      this.edgeMeta.rolesWithOutputType[contentType.pk][role.pk]--
    },
    rolesWithOutputType (contentType) {
      return Object.keys(
        this.edgeMeta.rolesWithOutputType[contentType.pk] ||
        {}).filter((rolePk) =>
        this.edgeMeta.rolesWithOutputType[contentType.pk][rolePk] > 0)
        .map((rolePk) => {
          return this.data[rolePk]
        })
    },
    rolesWithInputType (contentType) {
      return Object.keys(
        this.edgeMeta.rolesWithInputType[contentType.pk] ||
        {}).filter((rolePk) =>
        this.edgeMeta.rolesWithInputType[contentType.pk][rolePk] > 0)
        .map((rolePk) => {
          return this.data[rolePk]
        })
    },
    incrementEdge (inputRole, role, contentType) {
      const edgeHash = [
        inputRole.pk,
        role.pk,
        contentType.pk
      ].join(',')
      if (!this.edgeMeta.edgePresence[edgeHash]) {
        this.$set(this.edgeMeta.edgePresence, edgeHash, 0)
      }
      this.edgeMeta.edgePresence[edgeHash]++
      return this.edgeMeta.edgePresence[edgeHash]
    },
    decrementEdge (inputRole, role, contentType) {
      const edgeHash = [
        inputRole.pk,
        role.pk,
        contentType.pk
      ].join(',')
      this.edgeMeta.edgePresence[edgeHash]--
      return this.edgeMeta.edgePresence[edgeHash]
    },
    edgePushed (inputRole, role, contentType) {
      const edgeHash = [
        inputRole.pk,
        role.pk,
        contentType.pk
      ].join(',')
      return this.edgeMeta.edgePushed[edgeHash]
    },
    edgeHash (inputRole, role, contentType) {
      return [
        inputRole.pk,
        role.pk,
        contentType.pk
      ].join(',')
    },
    popEdge (cy, assignment, inputRole, role, contentType) {
      const edgeHash = this.edgeHash(inputRole, role, contentType)
      if (this.edgeMeta.assignmentHasEdge[assignment.pk]) {
        this.edgeMeta.edgePushed[edgeHash] = false
        cy.remove(this.elements.pop())
      }
    },
    pushEdge (cy, assignment, inputRole, role, contentType) {
      const edgeHash = this.edgeHash(inputRole, role, contentType)
      this.edgeMeta.edgePushed[edgeHash] = true
      this.edgeMeta.assignmentHasEdge[assignment.pk] = true
      this.elements.push(cy.add({
        data: this.edgeData(inputRole, role, contentType)
      }))
    },
    hideEdge (cy, inputRole, role, contentType) {
      const edgeHash = this.edgeHash(inputRole, role, contentType)
      this.toggleElement(cy, edgeHash, true)
    },
    showEdge (cy, inputRole, role, contentType) {
      const edgeHash = this.edgeHash(inputRole, role, contentType)
      this.toggleElement(cy, edgeHash, false)
    },
    toggleEdges (cy, assignment, valueTo) {
      const role = this.data[assignment.fields.role]
      // const responsibility = this.data[assignment.fields.responsibility]
      // const outputType = this.data[responsibility.fields.output_type]
      const inputTypes = this.inputTypes(assignment.fields.responsibility)

      if (valueTo) {
        // this.decrementRoleOutputType(role, outputType)
        inputTypes.forEach((inputType) => {
          this.rolesWithOutputType(inputType).forEach(
            (inputRole) => {
              const edgeCount = this.decrementEdge(
                inputRole, role, inputType)
              if (edgeCount <= 0) {
                this.hideEdge(cy, inputRole, role, inputType)
              }
            })
          this.decrementRoleInputType(role, inputType)
        })
        // this.rolesWithInputType(outputType).forEach(
        //   (outputRole) => {
        //     const edgeCount = this.decrementEdge(
        //       role, outputRole, outputType)
        //     if (edgeCount <= 0) {
        //       this.hideEdge(cy, role, outputRole, outputType)
        //     }
        //   })
      } else {
        // this.incrementRoleOutputType(role, outputType)
        inputTypes.forEach((inputType) => {
          this.rolesWithOutputType(inputType).forEach((inputRole) => {
            this.incrementEdge(inputRole, role, inputType)
            this.showEdge(cy, inputRole, role, inputType)
          })
          this.incrementRoleInputType(role, inputType)
        })
        // this.rolesWithInputType(outputType).forEach(
        //   (outputRole) => {
        //     this.incrementEdge(role, outputRole, outputType)
        //     this.showEdge(cy, role, outputRole, outputType)
        //   })
      }
    },
    edgeData (inputRole, role, contentType) {
      const edgeHash = this.edgeHash(inputRole, role, contentType)
      return {
        'id': edgeHash,
        'name': [
          this.data[contentType.fields.facet].fields.name,
          this.data[contentType.fields.format].fields.name
        ].join(' :: '),
        'source': inputRole.pk,
        'target': role.pk,
        'content_type': contentType.pk,
        'source_color': this.roleColor(inputRole),
        'target_color': this.roleColor(role),
        'classes': 'autorotate',
        'line_color': '#666'
      }
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
              this.roles.push(instance.pk)
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
            case 'role_model.responsibilityinputtype':
              const responsibilityId = e.instance.fields.responsibility
              if (!(responsibilityId in this.responsibilityInputTypes)) {
                this.$set(this.responsibilityInputTypes, responsibilityId, {})
              }
              this.$set(
                this.responsibilityInputTypes[responsibilityId],
                e.instance.pk, this.data[e.instance.fields.content_type])
              break
            case 'role_model.assignment':
              const role = this.data[instance.fields.role]
              const responsibility = this.data[instance.fields.responsibility]
              const outputType = this.data[responsibility.fields.output_type]
              const inputTypes = this.inputTypes(
                instance.fields.responsibility)

              this.incrementRoleOutputType(role, outputType)
              inputTypes.forEach((inputType) => {
                this.incrementRoleInputType(role, inputType)
                this.rolesWithOutputType(inputType).forEach((inputRole) => {
                  this.incrementEdge(inputRole, role, inputType)
                  if (!this.edgePushed(inputRole, role, inputType)) {
                    this.pushEdge(cy, instance, inputRole, role, inputType)
                  }
                })
              })
              // this.rolesWithInputType(outputType).forEach((outputRole) => {
              //   this.incrementEdge(role, outputRole, outputType)
              //   if (!this.edgePushed(role, outputRole, outputType)) {
              //     this.pushEdge(cy, instance, role, outputRole, outputType)
              //   }
              // })

              /*
              On Push
              Increment edge presence for each role output to this assignment's inputs.

              if (== 0) pushEdge

              On Pop
              Decrement edge presence for each role output to this assignment's inputs.

              if (== 1) popEdge

              On Delete
              Decrement edge presence for each role output to this assignment's inputs.
              Decrement edge presence for each role input from this assignment's output.

              if (== 0) hideEdge

              On Undelete
              Increment edge presence for each role output to this assignment's inputs.
              Increment edge presence for each role input from this assignment's output.

              if (> 0) showEdge
              */

              break
          }
          this.runLayout(cy)
        })
      }
      if (e.event === 'modified') {
        this.$cytoscape.instance.then(cy => {
          for (var field in e.changes) {
            if (e.changes.hasOwnProperty(field)) {
              const change = e.changes[field]
              const valueTo = change[0]
              this.data[e.instance.pk].fields[field] = valueTo
              if (field === 'is_deleted') {
                switch (e.instance.model) {
                  case 'role_model.assignment':
                    this.toggleEdges(cy, e.instance, valueTo)
                    break
                  default:
                    this.toggleElement(cy, e.instance.pk, valueTo)
                }
              }
            }
          }
        })
      }
    },
    popEvent () {
      var e = this.appliedEvents.pop()
      this.$cytoscape.instance.then(cy => {
        if (e.event === 'created') {
          const instance = e.instance
          if (e.instance.model === 'role_model.role' ||
              e.instance.model === 'role_model.group') {
            this.$cytoscape.instance.then(cy => {
              this.popNode(cy)
              this.runLayout(cy)
            })
          }
          if (e.instance.model === 'role_model.role') {
            this.roles.pop()
          }
          if (e.instance.model === 'role_model.group') {
            this.$delete(this.group_colors, e.instance.pk)
          }
          if (e.instance.model === 'role_model.assignment') {
            const role = this.data[instance.fields.role]
            const responsibility = this.data[instance.fields.responsibility]
            const outputType = this.data[responsibility.fields.output_type]
            const inputTypes = this.inputTypes(
              instance.fields.responsibility)

            this.decrementRoleOutputType(role, outputType)
            inputTypes.forEach((inputType) => {
              this.decrementRoleInputType(role, inputType)
              this.rolesWithOutputType(inputType).forEach((inputRole) => {
                this.decrementEdge(inputRole, role, inputType)
                this.popEdge(cy, instance, inputRole, role, inputType)
              })
            })
          }
          this.$delete(this.data, e.instance.pk)
        }

        if (e.event === 'modified') {
          for (var field in e.changes) {
            if (e.changes.hasOwnProperty(field)) {
              const change = e.changes[field]
              const valueFrom = change[1]
              this.data[e.instance.pk].fields[field] = valueFrom
              if (field === 'is_deleted') {
                switch (e.instance.model) {
                  case 'role_model.assignment':
                    this.toggleEdges(cy, e.instance, valueFrom)
                    break
                  default:
                    this.toggleElement(cy, e.instance.pk, valueFrom)
                }
              }
            }
          }
        }
      })
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
      edgeMeta: {
        rolesWithOutputType: {},
        rolesWithInputType: {},
        edgePresence: {},
        edgePushed: {},
        assignmentHasEdge: {}
      },
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
      responsibilityInputTypes: {},
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
            selector: '[name]',
            css: {
              'content': 'data(name)'
            }
          },
          {
            selector: 'node',
            css: {
              'shape': 'roundrectangle',
              'padding': '5',
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
              'target-arrow-shape': 'triangle',
              'control-point-step-size': '150px',
              'curve-style': 'bezier',
              'opacity': 0.9,
              'width': '5',
              'arrow-scale': 2.5,
              'source-arrow-shape': 'circle',
              'line-color': 'data(line_color)',
              'color': 'white',
              'text-outline-width': '3',
              'text-outline-color': 'black',
              'font-size': '24',
              'source-arrow-color': 'data(source_color)',
              'target-arrow-color': 'data(source_color)',
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
  cursor: pointer;
}

div {
  display: flex;
  align-items: stretch;
}
div.block {
  display: block;
  text-align: center;
}
#contact {
  background: #4F86F7;
  color: white;
  display: table;
}
#contact h2 {
  display: table-cell;
  vertical-align: middle;
}
#contact ul {
  list-style-type: none;
  padding: 0;
  font-size: 24px;
}
#contact a {
  color: white;
}
#content {
  display: block;
}
#content, #contact {
  width: 100%;
  padding: 20px;
  min-height: 100vh;
  transition: all 0.3s;
}
</style>
