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
      <v-col>
        <v-slider v-model="sliderMode" :max="max" :min="min" :step="step" thumb-label @change="onSliderModeStopped">
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
      <v-col cols="4" class="mr-auto">
        <v-card class="pa-2" outlined tile>
          <v-text-field
            ref="modeValue"
            @keydown="onTextModeEnterPressed"
            @blur="updateOnTextModeChange"
            v-model="textMode"
            label="Mode"
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
import BetaPERT from '@/implementations/parameter/distribution/BetaPERT';
import { Key } from 'ts-keycode-enum';

@Component
export default class BetaPertDisplay extends Vue implements IParameterDisplay {
  @Prop({ required: true }) parameterValue!: BetaPERT;

  sliderValue = [0, 0];

  sliderMode = 0;

  textMin = '';

  textMax = '';

  textMode = '';

  min = -100;

  max = 10000;

  step = 0.1;

  ignoreNextValueSliderChange = false;

  ignoreNextModeSliderChange = false;

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
    Vue.set(this.parameterValue, 'min', newValue[0]);
    Vue.set(this.parameterValue, 'max', newValue[1]);
    if (newValue[0] > this.sliderMode) {
      [this.sliderMode] = newValue;
    }
    if (newValue[1] < this.sliderMode) {
      [, this.sliderMode] = newValue;
    }
  }

  @Watch('sliderMode')
  onSliderModeChanged(newValue: number): void {
    if (this.ignoreNextModeSliderChange) {
      this.ignoreNextModeSliderChange = false;
      return;
    }

    this.textMode = newValue.toString();
    Vue.set(this.parameterValue, 'mode', newValue);
    if (newValue < this.sliderValue[0]) {
      this.sliderValue = [newValue, this.sliderValue[1]];
    }
    if (newValue > this.sliderValue[1]) {
      this.sliderValue = [this.sliderValue[0], newValue];
    }
  }

  @Watch('parameterValue')
  onParameterChanged(newValue: BetaPERT): void {
    this.min = this.parameterValue.metaData.lowerLimit ?? -100 + (this.parameterValue.min ?? 0);
    this.max = this.parameterValue.metaData.upperLimit ?? 100 + (this.parameterValue.max ?? 0);
    this.step = this.parameterValue.metaData.step ?? Math.max((this.max - this.min) / 1000, 0.1);

    this.ignoreNextValueSliderChange = true;
    this.sliderValue = [this.min, this.min];
    this.sliderValue = [newValue.min ?? this.min, newValue.max ?? this.max];

    this.ignoreNextModeSliderChange = true;
    this.sliderMode = this.min;
    this.sliderMode = newValue.mode ?? (this.min + this.max) / 2.0;

    this.textMin = newValue.min?.toString() ?? '';
    this.textMax = newValue.max?.toString() ?? '';
    this.textMode = newValue.mode?.toString() ?? '';
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

  onTextModeEnterPressed(event: KeyboardEvent): void {
    if (event.keyCode === Key.Enter) {
      this.updateOnTextModeChange();
    }
  }

  updateOnTextMinChange(): void {
    const value = Number(this.textMin);

    // eslint-disable-next-line @typescript-eslint/no-explicit-any
    const castComponent = this.$refs.minValue as any;
    if (this.textMin === '') {
      this.parameterValue.min = undefined;
    } else if (value === this.sliderValue[0]) {
      this.parameterValue.min = value;
    } else if (!this.parameterValue.isSet && !castComponent.validate(true)) {
      this.textMin = '';
    } else if (castComponent.validate && castComponent.validate(true)) {
      if (value >= this.sliderMode) {
        this.sliderMode = value;
        this.textMode = value.toString();
      }
      if (value >= this.sliderValue[1]) {
        this.sliderValue = [value, value];
        this.parameterValue.min = value;
        this.parameterValue.max = value;
      } else {
        this.sliderValue = [value, this.sliderValue[1]];
        this.parameterValue.min = value;
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
      this.parameterValue.max = undefined;
    } else if (value === this.sliderValue[1]) {
      this.parameterValue.max = value;
    } else if (!this.parameterValue.isSet && !castComponent.validate(true)) {
      this.textMax = '';
    } else if (castComponent.validate && castComponent.validate(true)) {
      if (value <= this.sliderMode) {
        this.sliderMode = value;
        this.textMode = value.toString();
      }
      if (value <= this.sliderValue[0]) {
        this.sliderValue = [value, value];
        this.parameterValue.min = value;
        this.parameterValue.max = value;
      } else {
        this.sliderValue = [this.sliderValue[0], value];
        this.parameterValue.max = value;
      }
    } else {
      this.textMax = this.sliderValue[1].toString();
    }
  }

  updateOnTextModeChange(): void {
    const value = Number(this.textMode);

    // eslint-disable-next-line @typescript-eslint/no-explicit-any
    const castComponent = this.$refs.modeValue as any;
    if (this.textMode === '') {
      this.parameterValue.mode = undefined;
    } else if (value === this.sliderMode) {
      this.parameterValue.mode = value;
    } else if (!this.parameterValue.isSet && !castComponent.validate(true)) {
      this.textMode = '';
    } else if (castComponent.validate && castComponent.validate(true)) {
      if (value >= this.sliderValue[1]) {
        this.sliderValue = [this.sliderValue[0], value];
      } else if (value <= this.sliderValue[0]) {
        this.sliderValue = [value, this.sliderValue[1]];
      }
      this.sliderMode = value;
    } else {
      this.textMode = this.sliderMode.toString();
    }
  }

  onSliderStopped(value: number[]): void {
    Vue.set(this.parameterValue, 'min', value[0]);
    Vue.set(this.parameterValue, 'max', value[1]);
  }

  onSliderModeStopped(value: number): void {
    Vue.set(this.parameterValue, 'mode', value);
  }

  setValues(): void {
    this.min = this.parameterValue.metaData.lowerLimit ?? -100 + (this.parameterValue.min ?? 0);
    this.max = this.parameterValue.metaData.upperLimit ?? 100 + (this.parameterValue.max ?? 0);

    this.ignoreNextValueSliderChange = true;
    this.sliderValue = [this.min, this.min];
    this.sliderValue = [this.parameterValue.min ?? this.min, this.parameterValue.max ?? this.max];

    this.ignoreNextModeSliderChange = true;
    this.sliderMode = this.min;
    this.sliderMode = this.parameterValue.mode ?? (this.min + this.max) / 2.0;

    this.step = this.parameterValue.metaData.step ?? Math.max((this.max - this.min) / 1000, 0.1);
    this.textMin = this.parameterValue.min?.toString() ?? '';
    this.textMax = this.parameterValue.max?.toString() ?? '';
    this.textMode = this.parameterValue.mode?.toString() ?? '';
  }

  created(): void {
    this.setValues();
  }
}
</script>

<style scoped lang="scss"></style>
