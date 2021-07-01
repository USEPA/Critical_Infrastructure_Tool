<template>
  <v-list>
    <v-list-item-group>
      <v-list-group active-class="secondary--text" v-for="(item, i) in getFilters()" :key="i">
        <template v-slot:activator>
          <v-list-item-icon>
            <v-badge
              offset-y="20"
              v-if="item.numberInvalidParameters() > 0"
              color="error"
              :content="item.numberInvalidParameters()"
            />
          </v-list-item-icon>
          <v-list-item-title>{{ item.name }}</v-list-item-title>
          <v-list-item-icon>
            <v-icon v-if="item.anyParameterChanged()">fa-edit</v-icon>
          </v-list-item-icon>
        </template>
        <parameter-filter-expansion-panel :filter="item" />
      </v-list-group>
    </v-list-item-group>
  </v-list>
</template>

<script lang="ts">
import Vue from 'vue';
import { Component, Prop } from 'vue-property-decorator';
import { State } from 'vuex-class';
import ParameterWrapperFilter from '@/implementations/parameter/ParameterWrapperFilter';
import ParameterWrapperList from '@/implementations/parameter/ParameterWrapperList';
import ParameterWrapper from '@/implementations/parameter/ParameterWrapper';
import ParameterFilterExpansionPanel from './ParameterFilterExpansionPanel.vue';

@Component({
  components: { ParameterFilterExpansionPanel },
})
export default class ParameterListExpansionPanel extends Vue {
  @State errorIcon!: string;

  @State currentSelectedParameter!: ParameterWrapper;

  @Prop()
  list!: ParameterWrapperList;

  getFilters(): ParameterWrapperFilter[] {
    return this.list.filters;
  }
}
</script>

<style scoped lang="scss"></style>
