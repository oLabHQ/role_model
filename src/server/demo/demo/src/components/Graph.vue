<template>
  <div>
    <Sidebar
      heading="Role Model">
      <SidebarMenu>
        <SidebarSubmenu>
          <SidebarSubmenuItem>Test</SidebarSubmenuItem>
          <SidebarSubmenuItem>Test</SidebarSubmenuItem>
        </SidebarSubmenu>
        <SidebarMenuItem>An Item</SidebarMenuItem>
      </SidebarMenu>
    </Sidebar>
    <div id="content">
    </div>
  </div>
</template>

<script>
import Sidebar from './Sidebar.vue'
import SidebarMenu from './SidebarMenu.vue'
import SidebarSubmenu from './SidebarSubmenu.vue'
import SidebarMenuItem from './SidebarMenuItem.vue'
import SidebarSubmenuItem from './SidebarSubmenuItem.vue'

export default {
  name: 'Graph',
  components: {
    Sidebar,
    SidebarMenu,
    SidebarSubmenu,
    SidebarMenuItem,
    SidebarSubmenuItem
  },
  data () {
    return {
      msg: 'Welcome to Your Vue.js App'
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
