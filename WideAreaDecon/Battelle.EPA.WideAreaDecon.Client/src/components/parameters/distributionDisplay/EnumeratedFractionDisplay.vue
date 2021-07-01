<template>
  <v-container>
    <v-row>
      <v-simple-table style="width: 100%">
        <template v-slot:default>
          <thead></thead>
          <tbody>
            <tr v-for="([key, value], index) in listOfParameterValues" :key="key">
              <td style="width: 20%" class="text-subtitle-1 text-center font-weight-medium">{{ key }}</td>
              <td style="width: 50%">
                <v-slider
                  class="large-slider"
                  v-model="value.value"
                  :disabled="values[index].locked"
                  :max="max"
                  :min="min"
                  :step="step"
                  thumb-label
                  @change="renormalize(value.value, index)"
                >
                </v-slider>
              </td>
              <td style="width: 20%">
                <v-card class="pa-2" outlined tile>
                  <v-text-field
                    :ref="`value-${index}`"
                    :disabled="values[index].locked"
                    @keydown="onTextEnterPressed($event, index)"
                    @blur="updateOnTextChange(index)"
                    v-model="values[index].text"
                    label="Value"
                    :rules="[validationRules]"
                    hide-details="auto"
                  >
                    <template v-slot:append>
                      <p class="grey--text">{{ value.metaData.units }}</p>
                    </template>
                  </v-text-field>
                </v-card>
              </td>
              <td style="width: 10%">
                <v-checkbox
                  v-model="value.locked"
                  off-icon="fa-lock-open"
                  on-icon="fa-lock"
                  color="grey"
                  :value="values[index].locked"
                  :ripple="false"
                  @click="lockRow(values[index].locked, index)"
                >
                </v-checkbox>
              </td>
            </tr>
          </tbody>
        </template>
      </v-simple-table>
    </v-row>
  </v-container>
</template>

<script lang="ts">
import Vue from 'vue';
import { Component, Prop, Watch } from 'vue-property-decorator';
import IParameterDisplay from '@/interfaces/component/IParameterDisplay';
import EnumeratedFraction from '@/implementations/parameter/list/enumeratedFraction';
import Constant from '@/implementations/parameter/distribution/Constant';
import { Key } from 'ts-keycode-enum';
import { clamp, sumBy } from 'lodash';

@Component
export default class EnumeratedFractionDisplay extends Vue implements IParameterDisplay {
  @Prop({ required: true }) parameterValue!: EnumeratedFraction;

  values: { value: number; locked: boolean; text: string }[] = [];

  max = 1;

  min = 0;

  step = 0.01;

  get listOfParameterValues(): [string, Constant][] {
    return Object.entries(this.parameterValue.values);
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

  renormalize(newValue: number, changedIndex: number): void {
    this.values[changedIndex].value = newValue;
    const normalizedFractions = this.normalize(changedIndex);

    // update values array w/ normalized values
    Object.entries(this.parameterValue.values).forEach(([category], i) => {
      this.values[i].value = normalizedFractions[i];
      this.values[i].text = normalizedFractions[i].toFixed(2);
      this.parameterValue.values[category].value = normalizedFractions[i];
    });
  }

  onTextEnterPressed(event: KeyboardEvent, index: number): void {
    if (event.keyCode === Key.Enter) {
      this.updateOnTextChange(index);
    }
  }

  updateOnTextChange(index: number): void {
    // eslint-disable-next-line @typescript-eslint/no-explicit-any
    const [castComponent] = this.$refs[`value-${index}`] as any;

    if (castComponent.validate && castComponent.validate(true)) {
      const value = +this.values[index].text;
      this.renormalize(value, index);
    }
  }

  normalize(changedIndex: number): number[] {
    const changedRow = this.values[changedIndex];
    // probability of locked rows
    const probLocked = sumBy(
      this.values.filter((v) => v.locked),
      (v) => v.value,
    );

    const unlockedRows = this.values.filter((v) => !v.locked);
    const probLeft = 1 - probLocked;
    changedRow.value = clamp(changedRow.value, unlockedRows.length > 1 ? 0 : probLeft, probLeft);
    const probUnlocked = sumBy(unlockedRows, (row) => row.value);

    const change = probUnlocked - probLeft;
    const otherUnlockProb = probUnlocked - changedRow.value;
    const numRowsToDisperse = this.values.filter((value) => !value.locked).length - 1;

    const normalizeFunc = this.getNormalizeFunc(change, otherUnlockProb, numRowsToDisperse);

    return this.values.map((v, i) => {
      if (v.locked || i === changedIndex) {
        return v.value;
      }

      return normalizeFunc(v.value);
    });
  }

  // eslint-disable-next-line class-methods-use-this
  getNormalizeFunc(change: number, otherUnlockProb: number, numRowsToDisperse: number): (x: number) => number {
    if (change === 0) {
      return (x) => x;
    }

    return change < 0
      ? (x) => x - change / numRowsToDisperse
      : (x) => x * ((otherUnlockProb - change) / otherUnlockProb);
  }

  lockRow(lockValue: boolean, index: number): void {
    const valueName = this.listOfParameterValues[index][0];
    this.parameterValue.values[valueName].locked = !lockValue;
    this.values[index].locked = !lockValue;
  }

  @Watch('parameterValue')
  onParameterChanged(): void {
    this.values = [];
    this.setValues();
  }

  setValues(): void {
    Object.values(this.parameterValue.values).forEach((constant: Constant) => {
      const value = constant.value ?? 0;
      const locked = constant.locked ?? false;
      const text = constant.value?.toFixed(2) ?? '';
      this.values.push({ value, locked, text });
    });
  }

  created(): void {
    this.setValues();
  }
}
</script>

<style lang="scss">
.large-slider .v-slider__track-container {
  height: 20px !important;
}
.large-slider .v-slider__track-fill {
  border-radius: 15px !important;
}
.large-slider .v-slider__track-background {
  border-radius: 15px !important;
}
.v-data-table__wrapper {
  overflow: visible !important;
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
