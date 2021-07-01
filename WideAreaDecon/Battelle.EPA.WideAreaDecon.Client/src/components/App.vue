<template>
  <v-app>
    <div>Hello world!</div>
    <nav-bar @showRunModal="showRunModal = true" />

    <!-- Content Router -->
    <v-main>
      <run-scenario v-model="showRunModal" />
      <router-view @showRunModal="showRunModal = true" />
    </v-main>

    <footer-bar />
  </v-app>
</template>

<script lang="ts">
import { Component, Vue } from 'vue-property-decorator';
import NavBar from '@/components/base/NavigationBar.vue';
import RunScenario from '@/components/modals/RunScenario.vue';
import FooterBar from '@/components/base/FooterBar.vue';

@Component({
  components: {
    NavBar,
    FooterBar,
    RunScenario,
  },
})
export default class App extends Vue {
  showRunModal = false;
}
</script>

<style scoped lang="scss">
.disabled-tool-tip {
  cursor: no-drop;
}
</style>
