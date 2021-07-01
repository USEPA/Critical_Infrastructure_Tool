<template>
  <v-dialog v-model="dialog" :max-width="maxWidth">
    <template v-slot:activator="{ on }">
      <v-icon v-on="on" @click="selectedHelpItem = item">help</v-icon>
    </template>
    <v-card class="mx-auto">
      <v-system-bar color="primary" height="60">
        <v-toolbar-title class="title">{{ item.title }} Info...</v-toolbar-title>
        <v-spacer />
        <v-icon @click="dialog = false" size="45">mdi-close</v-icon>
      </v-system-bar>
      <v-card-text class="body-1" v-text="item.helpMessage" />
    </v-card>
  </v-dialog>
</template>

<script lang="ts">
import Vue from 'vue';
import { Component, Prop } from 'vue-property-decorator';
import { State } from 'vuex-class';
import container from '@/dependencyInjection/config';
import IImageProvider from '@/interfaces/providers/IImageProvider';
import TYPES from '@/dependencyInjection/types';
import IHomeOptionsProvider from '@/interfaces/providers/IHomeOptionsProvider';
import IHomeOptions from '@/interfaces/configuration/IHomeOptions';

@Component
export default class HomeOptionHelp extends Vue {
  @Prop() item!: IHomeOptions;

  @Prop({ default: 600 }) maxWidth!: number;

  @State applicationTitle!: string;

  @State applicationSponsor!: string;

  dialog = false;

  data = container.get<IHomeOptionsProvider>(TYPES.HomeOptionsProvider).getOptions();

  selectedHelpItem?: IHomeOptions;

  // eslint-disable-next-line class-methods-use-this, @typescript-eslint/no-explicit-any
  getImage(name: string): any {
    return container.get<IImageProvider>(TYPES.ImageProvider).getImage(name);
  }
}
</script>

<style scoped lang="scss"></style>
