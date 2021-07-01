<template>
  <v-container :style="vuetifyColorProps()">
    <v-row
      ><v-col><v-spacer /></v-col
    ></v-row>
    <v-row>
      <v-col>
        <v-slider v-model="sliderValue" :max="max" :min="min" :step="step" thumb-label @change="onSliderStopped">
          <template v-slot:prepend>
            <p class="grey--text">{{ min }}</p>
          </template>
          <template v-slot:append>
            <p class="grey--text">{{ max }}</p>
          </template>
        </v-slider>
      </v-col>
    </v-row>
    <v-row>
      <v-col cols="4" class="mr-auto">
        <v-card class="pa-2" outlined tile>
          <v-text-field
            ref="value"
            @keydown="onTextEnterPressed"
            @blur="updateOnTextChange"
            v-model="textValue"
            label="Value"
            :rules="[validationRules]"
            hide-details="auto"
          >
            <template v-slot:append>
              <p class="grey--text">{{ parameterValue.metaData.units }}</p>
            </template>
          </v-text-field>
        </v-card>
      </v-col>
    </v-row>
  </v-container>
</template>

<script lang="ts">
import Vue from 'vue';
import { Component, Prop, Watch } from 'vue-property-decorator';
import IParameterDisplay from '@/interfaces/component/IParameterDisplay';
import Constant from '@/implementations/parameter/distribution/Constant';
import { Key } from 'ts-keycode-enum';

@Component
export default class ConstantParameterDisplay extends Vue implements IParameterDisplay {
  @Prop({ required: true }) parameterValue!: Constant;

  vuetifyColorProps(): unknown {
    return {
      '--primary-color': this.$vuetify.theme.currentTheme.primary,
    };
  }

  validationRules(value: string): boolean | string {
    const num = Number(value);
    if (Number.isNaN(num)) {
      return 'Value must be number!';
    }
    if (num > this.max) {
      return `Value must be less than or equal to ${this.max}`;
    }
    if (num < this.min) {
      return `Value must be greater than or equal to ${this.min}`;
    }
    return true;
  }

  sliderValue = 0;

  textValue = '';

  min = -100;

  max = 10000;

  step = 0.1;

  ignoreNextSliderChange = false;

  @Watch('sliderValue')
  onSliderValueChanged(newValue: number): void {
    if (!this.ignoreNextSliderChange) {
      this.textValue = newValue.toString();
      Vue.set(this.parameterValue, 'value', newValue);
    } else {
      this.ignoreNextSliderChange = false;
    }
  }

  @Watch('parameterValue')
  onParameterChanged(newValue: Constant): void {
    this.min = this.parameterValue.metaData.lowerLimit ?? -100;
    this.max = this.parameterValue.metaData.upperLimit ?? 100;
    this.step = this.parameterValue.metaData.step ?? Math.max((this.max - this.min) / 1000, 0.1);

    // this will force a value change update
    this.sliderValue = this.min;
    this.sliderValue = this.parameterValue.value ?? (this.min + this.max) / 2.0;

    this.ignoreNextSliderChange = true;

    this.textValue = newValue.value?.toString() ?? '';
  }

  onTextEnterPressed(event: KeyboardEvent): void {
    if (event.keyCode === Key.Enter) {
      this.updateOnTextChange();
    }
  }

  onSliderStopped(): void {
    Vue.set(this.parameterValue, 'value', this.sliderValue);
  }

  updateOnTextChange(): void {
    const value = Number(this.textValue);
    // eslint-disable-next-line @typescript-eslint/no-explicit-any
    const castComponent = this.$refs.value as any;
    if (this.textValue === '') {
      Vue.set(this.parameterValue, 'value', undefined);
    } else if (value === this.sliderValue) {
      Vue.set(this.parameterValue, 'value', value);
    } else if (!this.parameterValue.isSet && !castComponent.validate(true)) {
      this.textValue = '';
    } else if (castComponent.validate && castComponent.validate(true)) {
      this.sliderValue = value;
      Vue.set(this.parameterValue, 'value', value);
    } else {
      this.textValue = this.sliderValue.toString();
    }
  }

  setValues(): void {
    this.textValue = this.parameterValue.value?.toString() ?? '';
    this.min = this.parameterValue.metaData.lowerLimit ?? -100 + (this.sliderValue ?? 0);
    this.max = this.parameterValue.metaData.upperLimit ?? 100 + (this.sliderValue ?? 0);

    // this will force a value change update
    this.sliderValue = this.min;
    this.sliderValue = this.parameterValue.value ?? (this.min + this.max) / 2.0;

    this.ignoreNextSliderChange = true;

    this.step = this.parameterValue.metaData.step ?? Math.max((this.max - this.min) / 1000, 0.1);
  }

  created(): void {
    this.setValues();
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
