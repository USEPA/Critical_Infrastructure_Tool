<template>
  <v-navigation-drawer color="grey" class="lighten-2" clipped app :width="450">
    <parameter-list-expansion-panel :list="parameters" />
  </v-navigation-drawer>
</template>

<script lang="ts">
import Vue from 'vue';
import { Component, Prop } from 'vue-property-decorator';
import ParameterList from '@/implementations/parameter/ParameterList';
import ParameterListExpansionPanel from './ParameterListExpansionPanel.vue';

@Component({
  components: {
    ParameterListExpansionPanel,
  },
})
export default class ParameterSelectionDrawer extends Vue {
  @Prop({ required: true }) parameters!: ParameterList;
}
</script>

<style scoped lang="scss"></style>
