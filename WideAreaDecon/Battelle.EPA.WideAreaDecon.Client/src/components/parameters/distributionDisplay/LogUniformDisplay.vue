<template>
  <v-container :style="vuetifyColorProps()">
    <v-row>
      <v-col>
        <v-range-slider v-model="sliderValue" :max="max" :min="min" :step="step" thumb-label @change="onSliderStopped">
          <template v-slot:prepend>
            <p class="grey--text">{{ min }}</p>
          </template>
          <template v-slot:append>
            <p class="grey--text">{{ max }}</p>
          </template>
        </v-range-slider>
      </v-col>
    </v-row>
    <v-row>
      <v-col cols="4" class="mr-auto">
        <v-card class="pa-2" outlined tile>
          <v-text-field
            ref="minValue"
            @keydown="onTextMinEnterPressed"
            @blur="updateOnTextMinChange"
            v-model="textMin"
            label="Min"
            :rules="[validationRules]"
            hide-details="auto"
          >
            <template v-slot:append>
              <p class="grey--text">{{ parameterValue.metaData.units }}</p>
            </template>
          </v-text-field>
        </v-card>
      </v-col>
      <v-col cols="4" class="auto">
        <v-card class="pa-2" outlined tile>
          <v-text-field
            ref="maxValue"
            @keydown="onTextMaxEnterPressed"
            @blur="updateOnTextMaxChange"
            v-model="textMax"
            label="Max"
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
import { Key } from 'ts-keycode-enum';
import LogUniform from '@/implementations/parameter/distribution/LogUniform';

@Component
export default class LogUniformDisplay extends Vue implements IParameterDisplay {
  @Prop({ required: true }) parameterValue!: LogUniform;

  sliderValue = [0, 0];

  textMin = '';

  textMax = '';

  min = -100;

  max = 10000;

  step = 0.1;

  ignoreNextValueSliderChange = false;

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

  @Watch('sliderValue')
  onSliderValueChanged(newValue: number[]): void {
    if (this.ignoreNextValueSliderChange) {
      this.ignoreNextValueSliderChange = false;
      return;
    }
    this.textMin = newValue[0].toString();
    this.textMax = newValue[1].toString();
    Vue.set(this.parameterValue, 'logMin', Math.log10(newValue[0]));
    Vue.set(this.parameterValue, 'logMax', Math.log10(newValue[1]));
  }

  @Watch('parameterValue')
  onParameterChanged(newValue: LogUniform): void {
    this.min = this.parameterValue.metaData.lowerLimit ?? -100 + (this.parameterValue.min ?? 0);
    this.max = this.parameterValue.metaData.upperLimit ?? 100 + (this.parameterValue.max ?? 0);

    this.ignoreNextValueSliderChange = true;
    this.sliderValue = [this.min, this.min];
    this.sliderValue = [newValue.min ?? this.min, newValue.max ?? this.max];

    this.textMin = newValue.min?.toString() ?? '';
    this.textMax = newValue.max?.toString() ?? '';
    this.step = this.parameterValue.metaData.step ?? Math.max((this.max - this.min) / 1000, 0.1);
  }

  onTextMinEnterPressed(event: KeyboardEvent): void {
    if (event.keyCode === Key.Enter) {
      this.updateOnTextMinChange();
    }
  }

  onTextMaxEnterPressed(event: KeyboardEvent): void {
    if (event.keyCode === Key.Enter) {
      this.updateOnTextMaxChange();
    }
  }

  updateOnTextMinChange(): void {
    const value = Number(this.textMin);

    // eslint-disable-next-line @typescript-eslint/no-explicit-any
    const castComponent = this.$refs.minValue as any;
    if (this.textMin === '') {
      this.parameterValue.logMin = undefined;
    } else if (value === this.sliderValue[0]) {
      this.parameterValue.logMin = Math.log10(value);
    } else if (!this.parameterValue.isSet && !castComponent.validate(true)) {
      this.textMin = '';
    } else if (castComponent.validate && castComponent.validate(true)) {
      if (this.sliderValue[1] <= value) {
        this.sliderValue = [value, value];
        this.parameterValue.logMin = Math.log10(value);
        this.parameterValue.logMin = Math.log10(value);
      } else {
        this.sliderValue = [value, this.sliderValue[1]];
        this.parameterValue.logMin = Math.log10(value);
      }
    } else {
      this.textMin = this.sliderValue[0].toString();
    }
  }

  updateOnTextMaxChange(): void {
    const value = Number(this.textMax);

    // eslint-disable-next-line @typescript-eslint/no-explicit-any
    const castComponent = this.$refs.maxValue as any;
    if (this.textMax === '') {
      this.parameterValue.logMax = undefined;
    } else if (value === this.sliderValue[1]) {
      this.parameterValue.logMax = Math.log10(value);
    } else if (!this.parameterValue.isSet && !castComponent.validate(true)) {
      this.textMax = '';
    } else if (castComponent.validate && castComponent.validate(true)) {
      if (this.sliderValue[0] >= value) {
        this.sliderValue = [value, value];
        this.parameterValue.logMin = Math.log10(value);
        this.parameterValue.logMax = Math.log10(value);
      } else {
        this.sliderValue = [this.sliderValue[0], value];
        this.parameterValue.logMax = Math.log10(value);
      }
    } else {
      this.textMax = this.sliderValue[1].toString();
    }
  }

  onSliderStopped(value: number[]): void {
    Vue.set(this.parameterValue, 'logMin', Math.log10(value[0]));
    Vue.set(this.parameterValue, 'logMax', Math.log10(value[1]));
  }

  setValues(): void {
    this.min = this.parameterValue.metaData.lowerLimit ?? -100 + (this.parameterValue.min ?? 0);
    this.max = this.parameterValue.metaData.upperLimit ?? 100 + (this.parameterValue.max ?? 0);
    this.step = this.parameterValue.metaData.step ?? Math.max((this.max - this.min) / 1000, 0.1);

    this.ignoreNextValueSliderChange = true;
    this.sliderValue = [this.min, this.min];
    this.sliderValue = [this.parameterValue.min ?? 0, this.parameterValue.max ?? 1];

    this.textMin = this.parameterValue.min?.toString() ?? '';
    this.textMax = this.parameterValue.max?.toString() ?? '';
  }

  created(): void {
    this.setValues();
  }
}
</script>

<style scoped lang="scss"></style>
