<template>
  <div>
    <Sidebar
      heading="Acme Ltd">
      <SidebarMenu>
        <SidebarMenuItem
          href="http://google.com">Organization Chart</SidebarMenuItem>
        <SidebarSubmenu name="Roles">
          <SidebarSubmenuItem
            href="http://google.com">Test</SidebarSubmenuItem>
          <SidebarSubmenuItem
            href="http://google.com">Test</SidebarSubmenuItem>
        </SidebarSubmenu>
      </SidebarMenu>
    </Sidebar>
    <div id="content">
      {{ organizationEvents }}
    </div>
  </div>
</template>

<script>
import gql from 'graphql-tag'

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
        id,
        fields,
        event,
        instance
      }
    }`
  },
  data () {
    return {
      organizationEvents: []
    }
  }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
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
