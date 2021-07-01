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
      <v-col cols="6" class="auto">
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
import TruncatedNormal from '@/implementations/parameter/distribution/TruncatedNormal';
import { max } from 'lodash';

@Component
export default class TruncatedNormalDisplay extends Vue implements IParameterDisplay {
  @Prop({ required: true }) parameterValue!: TruncatedNormal;

  sliderValue = [0, 0];

  sliderMean = 0;

  sliderStd = 0;

  textMin = '';

  textMax = '';

  textMean = '';

  textStd = '';

  min = -100;

  max = 10000;

  step = 0.1;

  ignoreNextValueSliderChange = false;

  ignoreNextMeanSliderChange = false;

  ignoreNextStdSliderChange = false;

  get stdDevStep(): number {
    return max([(this.sliderValue[1] - this.sliderValue[0]) / 100, 0.01]) ?? 0.01;
  }

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
    Vue.set(this.parameterValue, 'mean', newValue);
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
    Vue.set(this.parameterValue, 'stdDev', newValue);
  }

  @Watch('parameterValue')
  onParameterChanged(newValue: TruncatedNormal): void {
    this.min = this.parameterValue.metaData.lowerLimit ?? -100 + (this.parameterValue.min ?? 0);
    this.max = this.parameterValue.metaData.upperLimit ?? 100 + (this.parameterValue.max ?? 0);
    this.step = this.parameterValue.metaData.step ?? Math.max((this.max - this.min) / 1000, 0.1);

    this.ignoreNextValueSliderChange = true;
    this.sliderValue = [this.min, this.min];
    this.sliderValue = [newValue.min ?? this.min, newValue.max ?? this.max];

    this.ignoreNextMeanSliderChange = true;
    this.sliderMean = this.min;
    this.sliderMean = newValue.mean ?? (this.min + this.max) / 2.0;

    this.ignoreNextStdSliderChange = true;
    this.sliderStd = this.min;
    this.sliderStd = newValue.stdDev ?? (this.min + this.max) / 2.0;

    this.textMin = newValue.min?.toString() ?? '';
    this.textMax = newValue.max?.toString() ?? '';
    this.textMean = newValue.mean?.toString() ?? '';
    this.textStd = newValue.stdDev?.toString() ?? '';
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
      if (value >= this.sliderMean) {
        this.sliderMean = value;
        this.textMean = value.toString();
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
      if (value <= this.sliderMean) {
        this.sliderMean = value;
        this.textMean = value.toString();
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

  onSliderStopped(value: number[]): void {
    Vue.set(this.parameterValue, 'min', value[0]);
    Vue.set(this.parameterValue, 'max', value[1]);
  }

  onSliderMeanStopped(value: number): void {
    Vue.set(this.parameterValue, 'mean', value);
  }

  onSliderStdStopped(value: number): void {
    Vue.set(this.parameterValue, 'stdDev', value);
  }

  setValues(): void {
    this.min = this.parameterValue.metaData.lowerLimit ?? -100 + (this.parameterValue.min ?? 0);
    this.max = this.parameterValue.metaData.upperLimit ?? 100 + (this.parameterValue.max ?? 0);

    this.ignoreNextValueSliderChange = true;
    this.sliderValue = [this.min, this.min];
    this.sliderValue = [this.parameterValue.min ?? this.min, this.parameterValue.max ?? this.max];

    this.ignoreNextMeanSliderChange = true;
    this.sliderMean = this.min;
    this.sliderMean = this.parameterValue.mean ?? (this.min + this.max) / 2.0;

    this.ignoreNextStdSliderChange = true;
    this.sliderStd = this.min;
    this.sliderStd = this.parameterValue.stdDev ?? (this.max - this.min) / 5.0;

    this.step = this.parameterValue.metaData.step ?? Math.max((this.max - this.min) / 1000, 0.1);
    this.textMin = this.parameterValue.min?.toString() ?? '';
    this.textMax = this.parameterValue.max?.toString() ?? '';
    this.textMean = this.parameterValue.mean?.toString() ?? '';
    this.textStd = this.parameterValue.stdDev?.toString() ?? '';
  }

  created(): void {
    this.setValues();
  }
}
</script>

<style scoped lang="scss"></style>
