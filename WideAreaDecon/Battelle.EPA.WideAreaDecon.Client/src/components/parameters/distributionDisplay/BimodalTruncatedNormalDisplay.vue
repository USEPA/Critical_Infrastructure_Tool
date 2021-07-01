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
    <!-- First mean and standard deviation slider -->
    <v-row>
      <v-col>
        <v-slider v-model="sliderMean1" :max="max" :min="min" :step="step" thumb-label @change="onSliderMean1Stopped">
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
          v-model="sliderStd1"
          :max="max - min"
          :min="(max - min) / 1000"
          :step="stdDevStep"
          thumb-label
          @change="onSliderStd1Stopped"
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
    <!-- Second mean and standard deviation slider -->
    <v-row>
      <v-col>
        <v-slider v-model="sliderMean2" :max="max" :min="min" :step="step" thumb-label @change="onSliderMean2Stopped">
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
          v-model="sliderStd2"
          :max="max - min"
          :min="(max - min) / 1000"
          :step="stdDevStep"
          thumb-label
          @change="onSliderStd2Stopped"
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
    <!-- First mean and standard deviation text boxes-->
    <v-row>
      <v-col cols="6" class="mr-auto">
        <v-card class="pa-2" outlined tile>
          <v-text-field
            ref="meanValue1"
            @keydown="onTextMeanEnterPressed"
            @blur="updateOnTextMeanChange"
            v-model="textMean1"
            label="Mean 1"
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
            ref="stdValue1"
            @keydown="onTextStdEnterPressed"
            @blur="updateOnTextStdChange"
            v-model="textStd1"
            label="Standard Deviation 1"
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
    <!-- Second mean and standard deviation text boxes -->
    <v-row>
      <v-col cols="6" class="mr-auto">
        <v-card class="pa-2" outlined tile>
          <v-text-field
            ref="meanValue2"
            @keydown="onTextMeanEnterPressed"
            @blur="updateOnTextMeanChange"
            v-model="textMean2"
            label="Mean 2"
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
            ref="stdValue2"
            @keydown="onTextStdEnterPressed"
            @blur="updateOnTextStdChange"
            v-model="textStd2"
            label="Standard Deviation 2"
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
import BimodalTruncatedNormal from '@/implementations/parameter/distribution/BimodalTruncatedNormal';
import { max } from 'lodash';

@Component
export default class BimodalTruncatedNormalDisplay extends Vue implements IParameterDisplay {
  @Prop({ required: true }) parameterValue!: BimodalTruncatedNormal;

  sliderValue = [0, 0];

  sliderMean1 = 0;

  sliderStd1 = 0;

  sliderMean2 = 0;

  sliderStd2 = 0;

  textMin = '';

  textMax = '';

  textMean1 = '';

  textStd1 = '';

  textMean2 = '';

  textStd2 = '';

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
    [this.parameterValue.min, this.parameterValue.max] = newValue;
    if (newValue[0] > this.sliderMean1) {
      [this.sliderMean1] = newValue;
    }
    if (newValue[1] < this.sliderMean1) {
      [, this.sliderMean1] = newValue;
    }

    if (newValue[0] > this.sliderMean2) {
      [this.sliderMean2] = newValue;
    }
    if (newValue[1] < this.sliderMean2) {
      [, this.sliderMean2] = newValue;
    }
  }

  @Watch('sliderMean1')
  onSliderMean1Changed(newValue: number): void {
    if (this.ignoreNextMeanSliderChange) {
      this.ignoreNextMeanSliderChange = false;
      return;
    }

    this.textMean1 = newValue.toString();
    this.parameterValue.mean1 = newValue;
    if (newValue < this.sliderValue[0]) {
      this.sliderValue = [newValue, this.sliderValue[1]];
    }
    if (newValue > this.sliderValue[1]) {
      this.sliderValue = [this.sliderValue[0], newValue];
    }
  }

  @Watch('sliderMean2')
  onSliderMean2Changed(newValue: number): void {
    if (this.ignoreNextMeanSliderChange) {
      this.ignoreNextMeanSliderChange = false;
      return;
    }

    this.textMean2 = newValue.toString();
    this.parameterValue.mean2 = newValue;
    if (newValue < this.sliderValue[0]) {
      this.sliderValue = [newValue, this.sliderValue[1]];
    }
    if (newValue > this.sliderValue[1]) {
      this.sliderValue = [this.sliderValue[0], newValue];
    }
  }

  @Watch('sliderStd1')
  onSliderStd1Changed(newValue: number): void {
    if (this.ignoreNextStdSliderChange) {
      this.ignoreNextStdSliderChange = false;
      return;
    }

    this.textStd1 = newValue.toString();
    this.parameterValue.stdDev1 = newValue;
  }

  @Watch('sliderStd2')
  onSliderStd2Changed(newValue: number): void {
    if (this.ignoreNextStdSliderChange) {
      this.ignoreNextStdSliderChange = false;
      return;
    }

    this.textStd2 = newValue.toString();
    this.parameterValue.stdDev2 = newValue;
  }

  @Watch('parameterValue')
  onParameterChanged(newValue: BimodalTruncatedNormal): void {
    this.min = this.parameterValue.metaData.lowerLimit ?? -100 + (this.parameterValue.min ?? 0);
    this.max = this.parameterValue.metaData.upperLimit ?? 100 + (this.parameterValue.max ?? 0);
    this.step = this.parameterValue.metaData.step ?? Math.max((this.max - this.min) / 1000, 0.1);

    this.ignoreNextValueSliderChange = true;
    this.sliderValue = [this.min, this.min];
    this.sliderValue = [newValue.min ?? this.min, newValue.max ?? this.max];

    this.ignoreNextMeanSliderChange = true;
    this.sliderMean1 = this.min;
    this.sliderMean1 = newValue.mean1 ?? (this.min + this.max) / 4.0;

    this.sliderMean2 = this.min;
    this.sliderMean2 = newValue.mean2 ?? (this.min + this.max) / (4.0 / 3.0);

    this.ignoreNextStdSliderChange = true;
    this.sliderStd1 = this.min;
    this.sliderStd1 = newValue.stdDev1 ?? (this.min + this.max) / 2.0;

    this.sliderStd2 = this.min;
    this.sliderStd2 = newValue.stdDev2 ?? (this.min + this.max) / 2.0;

    this.textMin = newValue.min?.toString() ?? '';
    this.textMax = newValue.max?.toString() ?? '';
    this.textMean1 = newValue.mean1?.toString() ?? '';
    this.textStd1 = newValue.stdDev1?.toString() ?? '';
    this.textMean2 = newValue.mean2?.toString() ?? '';
    this.textStd2 = newValue.stdDev2?.toString() ?? '';
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
      if (value >= this.sliderMean1) {
        this.sliderMean1 = value;
        this.textMean1 = value.toString();
      }
      if (value >= this.sliderMean2) {
        this.sliderMean2 = value;
        this.textMean2 = value.toString();
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
      if (value <= this.sliderMean1) {
        this.sliderMean1 = value;
        this.textMean1 = value.toString();
      }
      if (value <= this.sliderMean2) {
        this.sliderMean2 = value;
        this.textMean2 = value.toString();
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
    const value1 = Number(this.textMean1);
    const value2 = Number(this.textMean2);

    // eslint-disable-next-line @typescript-eslint/no-explicit-any
    const castComponent1 = this.$refs.meanValue1 as any;
    if (this.textMean1 === '') {
      this.parameterValue.mean1 = undefined;
    } else if (value1 === this.sliderMean1) {
      this.parameterValue.mean1 = value1;
    } else if (!this.parameterValue.isSet && !castComponent1.validate(true)) {
      this.textMean1 = '';
    } else if (castComponent1.validate && castComponent1.validate(true)) {
      if (value1 >= this.sliderValue[1]) {
        this.sliderValue = [this.sliderValue[0], value1];
      } else if (value1 <= this.sliderValue[0]) {
        this.sliderValue = [value1, this.sliderValue[1]];
      }
      this.sliderMean1 = value1;
    } else {
      this.textMean1 = this.sliderMean1.toString();
    }

    // eslint-disable-next-line @typescript-eslint/no-explicit-any
    const castComponent2 = this.$refs.meanValue2 as any;
    if (this.textMean2 === '') {
      this.parameterValue.mean2 = undefined;
    } else if (value1 === this.sliderMean2) {
      this.parameterValue.mean2 = value1;
    } else if (!this.parameterValue.isSet && !castComponent2.validate(true)) {
      this.textMean2 = '';
    } else if (castComponent2.validate && castComponent2.validate(true)) {
      if (value2 >= this.sliderValue[1]) {
        this.sliderValue = [this.sliderValue[0], value2];
      } else if (value2 <= this.sliderValue[0]) {
        this.sliderValue = [value2, this.sliderValue[1]];
      }
      this.sliderMean2 = value2;
    } else {
      this.textMean2 = this.sliderMean2.toString();
    }
  }

  updateOnTextStdChange(): void {
    const value1 = Number(this.textStd1);
    const value2 = Number(this.textStd2);

    // eslint-disable-next-line @typescript-eslint/no-explicit-any
    const castComponent1 = this.$refs.stdValue1 as any;
    if (this.textStd1 === '') {
      this.parameterValue.stdDev1 = undefined;
    } else if (value1 === this.sliderStd1) {
      this.parameterValue.stdDev1 = value1;
    } else if (!this.parameterValue.isSet && !castComponent1.validate(true)) {
      this.textStd1 = '';
    } else {
      this.textStd1 = this.sliderStd1.toString();
    }

    // eslint-disable-next-line @typescript-eslint/no-explicit-any
    const castComponent2 = this.$refs.stdValue2 as any;
    if (this.textStd2 === '') {
      this.parameterValue.stdDev2 = undefined;
    } else if (value2 === this.sliderStd2) {
      this.parameterValue.stdDev2 = value2;
    } else if (!this.parameterValue.isSet && !castComponent2.validate(true)) {
      this.textStd2 = '';
    } else {
      this.textStd2 = this.sliderStd2.toString();
    }
  }

  onSliderStopped(value: number[]): void {
    [this.parameterValue.min, this.parameterValue.max] = value;
  }

  onSliderMean1Stopped(value: number): void {
    this.parameterValue.mean1 = value;
  }

  onSliderStd1Stopped(value: number): void {
    this.parameterValue.stdDev1 = value;
  }

  onSliderMean2Stopped(value: number): void {
    this.parameterValue.mean2 = value;
  }

  onSliderStd2Stopped(value: number): void {
    this.parameterValue.stdDev2 = value;
  }

  setValues(): void {
    this.min = this.parameterValue.metaData.lowerLimit ?? -100 + (this.parameterValue.min ?? 0);
    this.max = this.parameterValue.metaData.upperLimit ?? 100 + (this.parameterValue.max ?? 0);

    this.ignoreNextValueSliderChange = true;
    this.sliderValue = [this.min, this.min];
    this.sliderValue = [this.parameterValue.min ?? this.min, this.parameterValue.max ?? this.max];

    this.ignoreNextMeanSliderChange = true;
    this.sliderMean1 = this.min;
    this.sliderMean1 = this.parameterValue.mean1 ?? (this.min + this.max) / 4.0;

    this.sliderMean2 = this.min;
    this.sliderMean2 = this.parameterValue.mean2 ?? (this.min + this.max) / (4.0 / 3.0);

    this.ignoreNextStdSliderChange = true;
    this.sliderStd1 = this.min;
    this.sliderStd1 = this.parameterValue.stdDev ?? (this.max - this.min) / 5.0;

    this.sliderStd2 = this.min;
    this.sliderStd2 = this.parameterValue.stdDev2 ?? (this.max - this.min) / 5.0;

    this.step = this.parameterValue.metaData.step ?? Math.max((this.max - this.min) / 1000, 0.1);
    this.textMin = this.parameterValue.min?.toString() ?? '';
    this.textMax = this.parameterValue.max?.toString() ?? '';
    this.textMean1 = this.parameterValue.mean1?.toString() ?? '';
    this.textStd1 = this.parameterValue.stdDev1?.toString() ?? '';
    this.textMean2 = this.parameterValue.mean2?.toString() ?? '';
    this.textStd2 = this.parameterValue.stdDev2?.toString() ?? '';
  }

  created(): void {
    this.setValues();
  }
}
</script>

<style scoped lang="scss"></style>
