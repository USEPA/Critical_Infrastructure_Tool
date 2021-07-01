<template>
  <v-container :style="vuetifyColorProps()">
    <v-row
      ><v-col><v-spacer /></v-col
    ></v-row>
    <v-row>
      <v-col>
        <v-slider>
          <template v-slot:prepend>
            <p class="grey--text"></p>
          </template>
          <template v-slot:append>
            <p class="grey--text"></p>
          </template>
        </v-slider>
      </v-col>
    </v-row>
    <v-row>
      <v-col cols="4" class="mr-auto">
        <v-card class="pa-2" outlined tile>
          <v-text-field>
            <template v-slot:append>
              <p class="grey--text"></p>
            </template>
          </v-text-field>
        </v-card>
      </v-col>
    </v-row>
  </v-container>
</template>

<script lang="ts">
import Vue from 'vue';
import { Component, Prop } from 'vue-property-decorator';
import IParameterDisplay from '@/interfaces/component/IParameterDisplay';
import TextValue from '@/implementations/parameter/distribution/TextValue';

@Component
export default class TextParameterDisplay extends Vue implements IParameterDisplay {
  @Prop({ required: true }) parameterValue!: TextValue;

  vuetifyColorProps(): unknown {
    return {
      '--primary-color': this.$vuetify.theme.currentTheme.primary,
    };
  }

  // eslint-disable-next-line class-methods-use-this
  validationRules(value: string): boolean | string {
    const num = Number(value);
    if (!Number.isNaN(num)) {
      return 'Value must be text!';
    }
    return true;
  }
}
</script>

<style lang="scss">
.v-slider__track-container {
  height: 8px !important;
}
.v-slider__track-fill {
  border-radius: 5px !important;
}
.v-slider__track-background {
  border-radius: 5px !important;
}
.v-slider__thumb {
  width: 24px !important;
  height: 24px !important;
  left: -12px !important;
}
.v-slider__thumb:before {
  left: -6px !important;
  top: -6px !important;
}
.theme--light.v-card.v-card--outlined {
  border: 2px solid !important;
  border-color: var(--primary-color) !important;
  border-radius: 5px !important;
}
</style>

<style scoped lang="scss4"></style>
