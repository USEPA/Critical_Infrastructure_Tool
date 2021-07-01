<template>
  <v-container :style="vuetifyColorProps()">
    <v-row>
      <v-col>
        <v-slider v-model="sliderMean" :max="max" :min="min" :step="step" thumb-label @change="onSliderMeanStopped">
          <template v-slot:prepend>
            <p class="grey--text">{{ min }}</p>
          </template>
          <template v-slot:append>
            <p class="grey--text">{{ max }}</p>
          </template>
        </v-slider>
      </v-col>
      <v-col>
        <v-slider
          v-model="sliderStd"
          :max="max - min"
          :min="(max - min) / 1000"
          :step="stdDevStep"
          thumb-label
          @change="onSliderStdStopped"
        >
          <template v-slot:prepend>
            <p class="grey--text">{{ (max - min) / 1000 }}</p>
          </template>
          <template v-slot:append>
            <p class="grey--text">{{ max - min }}</p>
          </template>
        </v-slider>
      </v-col>
    </v-row>
    <v-row>
      <v-col cols="6" class="mr-auto">
        <v-card class="pa-2" outlined tile>
          <v-text-field
            ref="meanValue"
            @keydown="onTextMeanEnterPressed"
            @blur="updateOnTextMeanChange"
            v-model="textMean"
            label="Mean"
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
            ref="stdValue"
            @keydown="onTextStdEnterPressed"
            @blur="updateOnTextStdChange"
            v-model="textStd"
            label="Standard Deviation"
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
import LogNormal from '@/implementations/parameter/distribution/LogNormal';

@Component
export default class LogNormalDisplay extends Vue implements IParameterDisplay {
  @Prop({ required: true }) parameterValue!: LogNormal;

  sliderValue = [0, 0];

  sliderMean = 0;

  sliderStd = 0;

  textMean = '';

  textStd = '';

  step = 0.1;

  ignoreNextValueSliderChange = false;

  ignoreNextMeanSliderChange = false;

  ignoreNextStdSliderChange = false;

  get stdDevStep(): number {
    return max([(this.sliderValue[1] - this.sliderValue[0]) / 100, 0.01]) ?? 0.01;
  }

  get min(): number {
    return this.parameterValue.metaData.lowerLimit;
  }

  get max(): number {
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
    if (newValue[0] > this.sliderMean) {
      [this.sliderMean] = newValue;
    }
    if (newValue[1] < this.sliderMean) {
      [, this.sliderMean] = newValue;
    }
  }

  @Watch('sliderMean')
  onSliderMeanChanged(newValue: number): void {
    if (this.ignoreNextMeanSliderChange) {
      this.ignoreNextMeanSliderChange = false;
      return;
    }

    this.textMean = newValue.toString();
    Vue.set(this.parameterValue, 'mean', Math.log10(newValue));
    if (newValue < this.sliderValue[0]) {
      this.sliderValue = [newValue, this.sliderValue[1]];
    }
    if (newValue > this.sliderValue[1]) {
      this.sliderValue = [this.sliderValue[0], newValue];
    }
  }

  @Watch('sliderStd')
  onSliderStdChanged(newValue: number): void {
    if (this.ignoreNextStdSliderChange) {
      this.ignoreNextStdSliderChange = false;
      return;
    }

    this.textStd = newValue.toString();
    Vue.set(this.parameterValue, 'stdDev', Math.log10(newValue));
  }

  @Watch('parameterValue')
  onParameterChanged(newValue: LogNormal): void {
    this.step = this.parameterValue.metaData.step;

    this.ignoreNextValueSliderChange = true;

    this.ignoreNextMeanSliderChange = true;
    this.sliderMean = 0;
    this.sliderMean = newValue.mean ?? 1;

    this.ignoreNextStdSliderChange = true;
    this.sliderStd = 1;
    this.sliderStd = newValue.stdDev ?? 2;

    this.textMean = newValue.mean?.toString() ?? '';
    this.textStd = newValue.stdDev?.toString() ?? '';
  }

  onTextMeanEnterPressed(event: KeyboardEvent): void {
    if (event.keyCode === Key.Enter) {
      this.updateOnTextMeanChange();
    }
  }

  onTextStdEnterPressed(event: KeyboardEvent): void {
    if (event.keyCode === Key.Enter) {
      this.updateOnTextStdChange();
    }
  }

  updateOnTextMeanChange(): void {
    const value = Number(this.textMean);

    // eslint-disable-next-line @typescript-eslint/no-explicit-any
    const castComponent = this.$refs.meanValue as any;
    if (this.textMean === '') {
      this.parameterValue.mean = undefined;
    } else if (value === this.sliderMean) {
      this.parameterValue.mean = value;
    } else if (!this.parameterValue.isSet && !castComponent.validate(true)) {
      this.textMean = '';
    } else if (castComponent.validate && castComponent.validate(true)) {
      if (value >= this.sliderValue[1]) {
        this.sliderValue = [this.sliderValue[0], value];
      } else if (value <= this.sliderValue[0]) {
        this.sliderValue = [value, this.sliderValue[1]];
      }
      this.sliderMean = value;
    } else {
      this.textMean = this.sliderMean.toString();
    }
  }

  updateOnTextStdChange(): void {
    const value = Number(this.textStd);

    // eslint-disable-next-line @typescript-eslint/no-explicit-any
    const castComponent = this.$refs.stdValue as any;
    if (this.textStd === '') {
      this.parameterValue.stdDev = undefined;
    } else if (value === this.sliderStd) {
      this.parameterValue.stdDev = value;
    } else if (!this.parameterValue.isSet && !castComponent.validate(true)) {
      this.textStd = '';
    } else {
      this.textStd = this.sliderStd.toString();
    }
  }

  onSliderMeanStopped(value: number): void {
    Vue.set(this.parameterValue, 'mean', Math.log10(value));
  }

  onSliderStdStopped(value: number): void {
    Vue.set(this.parameterValue, 'stdDev', Math.log10(value));
  }

  setValues(): void {
    this.ignoreNextMeanSliderChange = true;
    this.sliderMean = 0;
    this.sliderMean = this.parameterValue.mean ?? 1;

    this.ignoreNextStdSliderChange = true;
    this.sliderStd = 2;
    this.sliderStd = this.parameterValue.stdDev ?? 1;

    this.step = this.parameterValue.metaData.step;
    this.textMean = this.parameterValue.mean?.toString() ?? '';
    this.textStd = this.parameterValue.stdDev?.toString() ?? '';
  }

  created(): void {
    this.setValues();
  }
}
</script>

<style scoped lang="scss"></style>
