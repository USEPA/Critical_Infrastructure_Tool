<template>
  <v-dialog v-model="dialogActive" persistent max-width="700">
    <v-card class="mx-auto" height="600">
      <v-system-bar color="primary" height="60">
        <v-toolbar-title class="title">Load Pre-Defined Scenario</v-toolbar-title>
        <v-spacer />
        <v-icon @click="closed()" size="45">mdi-close</v-icon>
      </v-system-bar>
      <v-card-text class="body-1">Page is under contsruction...</v-card-text>
    </v-card>
  </v-dialog>
</template>

<script lang="ts">
import Vue from 'vue';
import { Component, Prop } from 'vue-property-decorator';

@Component
export default class LoadPreDefinedScenario extends Vue {
  @Prop() dialogActive!: boolean;

  closed(): void {
    this.$emit('closed');
  }
}
</script>

<style scoped lang="scss"></style>
