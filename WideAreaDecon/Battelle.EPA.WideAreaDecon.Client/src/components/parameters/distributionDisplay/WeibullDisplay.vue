<template>
  <v-container :style="vuetifyColorProps()">
    <v-row>
      <v-col>
        <v-slider v-model="sliderLambda" :max="max" :min="min" :step="step" thumb-label @change="onSliderLambdaStopped">
          <template v-slot:prepend>
            <p class="grey--text">{{ min }}</p>
          </template>
          <template v-slot:append>
            <p class="grey--text">{{ max }}</p>
          </template>
        </v-slider>
      </v-col>
      <v-col>
        <v-slider v-model="sliderK" :max="max" :min="min" :step="KStep" thumb-label @change="onSliderKStopped">
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
      <v-col cols="6" class="mr-auto">
        <v-card class="pa-2" outlined tile>
          <v-text-field
            ref="LambdaValue"
            @keydown="onTextLambdaEnterPressed"
            @blur="updateOnTextLambdaChange"
            v-model="textLambda"
            label="Lambda"
            :rules="[validationRules]"
            hide-details="auto"
          >
            <template v-slot:append>
              <p class="grey--text">{{ parameterValue.metaData.units }}</p>
            </template>
          </v-text-field>
        </v-card>
      </v-col>
      <v-col cols="6" class="auto">
        <v-card class="pa-2" outlined tile>
          <v-text-field
            ref="KValue"
            @keydown="onTextKEnterPressed"
            @blur="updateOnTextKChange"
            v-model="textK"
            label="k"
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
import { max } from 'lodash';
import Weibull from '@/implementations/parameter/distribution/Weibull';

@Component
export default class WeibullDisplay extends Vue implements IParameterDisplay {
  @Prop({ required: true }) parameterValue!: Weibull;

  sliderValue = [0, 0];

  sliderLambda = 0;

  sliderK = 0;

  textLambda = '';

  textK = '';

  step = 0.1;

  ignoreNextValueSliderChange = false;

  ignoreNextLambdaSliderChange = false;

  ignoreNextKSliderChange = false;

  get KStep(): number {
    return max([(this.sliderValue[1] - this.sliderValue[0]) / 100, 0.01]) ?? 0.01;
  }

  // eslint-disable-next-line class-methods-use-this
  get min(): number {
    // return 0.0;
    return this.parameterValue.metaData.lowerLimit;
  }

  // eslint-disable-next-line class-methods-use-this
  get max(): number {
    // return 1000.0;
    return this.parameterValue.metaData.upperLimit;
  }

  vuetifyColorProps(): unknown {
    return {
      '--primary-color': this.$vuetify.theme.currentTheme.primary,
    };
  }

  // eslint-disable-next-line class-methods-use-this
  validationRules(value: string): boolean | string {
    const num = Number(value);
    if (Number.isNaN(num)) {
      return 'Value must be number!';
    }
    return true;
  }

  @Watch('sliderValue')
  onSliderValueChanged(newValue: number[]): void {
    if (this.ignoreNextValueSliderChange) {
      this.ignoreNextValueSliderChange = false;
      return;
    }
    if (newValue[0] > this.sliderLambda) {
      [this.sliderLambda] = newValue;
    }
    if (newValue[1] < this.sliderLambda) {
      [, this.sliderLambda] = newValue;
    }
  }

  @Watch('sliderLambda')
  onSliderLambdaChanged(newValue: number): void {
    if (this.ignoreNextLambdaSliderChange) {
      this.ignoreNextLambdaSliderChange = false;
      return;
    }

    this.textLambda = newValue.toString();
    Vue.set(this.parameterValue, 'lambda', Math.log10(newValue));
    if (newValue < this.sliderValue[0]) {
      this.sliderValue = [newValue, this.sliderValue[1]];
    }
    if (newValue > this.sliderValue[1]) {
      this.sliderValue = [this.sliderValue[0], newValue];
    }
  }

  @Watch('sliderK')
  onSliderKChanged(newValue: number): void {
    if (this.ignoreNextKSliderChange) {
      this.ignoreNextKSliderChange = false;
      return;
    }

    this.textK = newValue.toString();
    Vue.set(this.parameterValue, 'k', Math.log10(newValue));
  }

  @Watch('parameterValue')
  onParameterChanged(newValue: Weibull): void {
    this.step = this.parameterValue.metaData.step;

    this.ignoreNextValueSliderChange = true;

    this.ignoreNextLambdaSliderChange = true;
    this.sliderLambda = 0;
    this.sliderLambda = newValue.lambda ?? 1;

    this.ignoreNextKSliderChange = true;
    this.sliderK = 1;
    this.sliderK = newValue.k ?? 2;

    this.textLambda = newValue.lambda?.toString() ?? '';
    this.textK = newValue.k?.toString() ?? '';
  }

  onTextLambdaEnterPressed(event: KeyboardEvent): void {
    if (event.keyCode === Key.Enter) {
      this.updateOnTextLambdaChange();
    }
  }

  onTextKEnterPressed(event: KeyboardEvent): void {
    if (event.keyCode === Key.Enter) {
      this.updateOnTextKChange();
    }
  }

  updateOnTextLambdaChange(): void {
    const value = Number(this.textLambda);

    // eslint-disable-next-line @typescript-eslint/no-explicit-any
    const castComponent = this.$refs.LambdaValue as any;
    if (this.textLambda === '') {
      this.parameterValue.lambda = undefined;
    } else if (value === this.sliderLambda) {
      this.parameterValue.lambda = value;
    } else if (!this.parameterValue.isSet && !castComponent.validate(true)) {
      this.textLambda = '';
    } else if (castComponent.validate && castComponent.validate(true)) {
      if (value >= this.sliderValue[1]) {
        this.sliderValue = [this.sliderValue[0], value];
      } else if (value <= this.sliderValue[0]) {
        this.sliderValue = [value, this.sliderValue[1]];
      }
      this.sliderLambda = value;
    } else {
      this.textLambda = this.sliderLambda.toString();
    }
  }

  updateOnTextKChange(): void {
    const value = Number(this.textK);

    // eslint-disable-next-line @typescript-eslint/no-explicit-any
    const castComponent = this.$refs.KValue as any;
    if (this.textK === '') {
      this.parameterValue.k = undefined;
    } else if (value === this.sliderK) {
      this.parameterValue.k = value;
    } else if (!this.parameterValue.isSet && !castComponent.validate(true)) {
      this.textK = '';
    } else {
      this.textK = this.sliderK.toString();
    }
  }

  onSliderLambdaStopped(value: number): void {
    Vue.set(this.parameterValue, 'lambda', Math.log10(value));
  }

  onSliderKStopped(value: number): void {
    Vue.set(this.parameterValue, 'k', Math.log10(value));
  }

  setValues(): void {
    this.ignoreNextLambdaSliderChange = true;
    this.sliderLambda = 0;
    this.sliderLambda = this.parameterValue.lambda ?? 1;

    this.ignoreNextKSliderChange = true;
    this.sliderK = 2;
    this.sliderK = this.parameterValue.k ?? 1;

    this.step = this.parameterValue.metaData.step;
    this.textLambda = this.parameterValue.lambda?.toString() ?? '';
    this.textK = this.parameterValue.k?.toString() ?? '';
  }

  created(): void {
    this.setValues();
  }
}
</script>

<style scoped lang="scss"></style>
