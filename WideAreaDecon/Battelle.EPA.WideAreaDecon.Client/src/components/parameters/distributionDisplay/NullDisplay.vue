<template>
  <v-container fill-height fluid>
    <v-row align="center" justify="center">
      <v-col>
        <p class="text-center display-3">Select a parameter to edit from the left menu...</p>
      </v-col>
    </v-row>
  </v-container>
</template>

<script lang="ts">
import Vue from 'vue';
import { Component, Prop } from 'vue-property-decorator';
import IParameterDisplay from '@/interfaces/component/IParameterDisplay';
import IParameter from '@/interfaces/parameter/IParameter';

@Component
export default class NullParameterDisplay extends Vue implements IParameterDisplay {
  @Prop({ required: true }) parameterValue!: IParameter;
}
</script>

<style scoped lang="scss"></style>
