<template>
  <v-container :style="vuetifyColorProps()">
    <v-row>
      <v-col align="center">
        <v-btn v-if="selectedSet.points.length < 6" @click="addPoint">Add Point</v-btn>
      </v-col>
      <v-col align="center">
        <v-btn-toggle v-model="selectedSetName" dense mandatory background-color="primary">
          <v-btn v-for="set in variableSets" :key="set.name" :value="set.name">{{ set.name }}</v-btn>
        </v-btn-toggle>
      </v-col>
    </v-row>
    <v-card v-if="displayChart" flat class="pa-5" tile width="100%" height="400">
      <scatter-plot-wrapper :options="chartOptions" :data="chartData" :type="'scatter'" :width="400" :height="150" />
    </v-card>
    <v-row v-if="editPoint">
      <v-col>
        <v-card class="pa-2" outlined tile>
          <v-text-field
            type="number"
            disabled
            v-model.number="selectedSet.points[selectedIndex]"
            :label="selectedSetName"
            hide-details="auto"
          ></v-text-field>
        </v-card>
      </v-col>
      <v-col>
        <v-card class="pa-2" outlined tile>
          <v-text-field
            @input="updateOnTextChange($event, 'min', selectedSet.indices[selectedIndex])"
            :rules="[validationRulesMin]"
            type="number"
            :value="selectedSet.mins[selectedIndex]"
            :label="`Min ${parameterValue.metaData.name}`"
            hide-details="auto"
          ></v-text-field>
        </v-card>
      </v-col>
      <v-col>
        <v-card class="pa-2" outlined tile>
          <v-text-field
            @input="updateOnTextChange($event, 'max', selectedSet.indices[selectedIndex])"
            :rules="[validationRulesMax]"
            type="number"
            :value="selectedSet.maxs[selectedIndex]"
            :label="`Max ${parameterValue.metaData.name}`"
            hide-details="auto"
          ></v-text-field>
        </v-card>
      </v-col>
      <v-col>
        <v-btn
          :disabled="
            selectedSet.points.length <= 2 || selectedIndex <= 0 || selectedIndex === selectedSet.points.length - 1
          "
          @click="removePoint(selectedSet.indices[selectedIndex])"
        >
          Remove Point
        </v-btn>
      </v-col>
    </v-row>
  </v-container>
</template>

<script lang="ts">
import Vue from 'vue';
import { Component, Prop, Watch } from 'vue-property-decorator';
import IParameterDisplay from '@/interfaces/component/IParameterDisplay';
import UniformXDependent from '@/implementations/parameter/distribution/UniformXDependent';
import {
  ScatterPlotWrapper,
  ChartPoint2D,
  CycleColorProvider,
  ScatterChartDataset,
  DefaultChartOptions,
  DefaultChartData,
} from 'battelle-common-vue-charting/src';
import Chart, { ChartLegendLabelItem } from 'chart.js';

@Component({ components: { ScatterPlotWrapper } })
export default class UniformXDependentDisplay extends Vue implements IParameterDisplay {
  @Prop({ required: true }) parameterValue!: UniformXDependent;

  key = this.$vnode.key;

  baseline!: UniformXDependent;

  editPoint = false;

  selectedIndex = -1;

  chartOptions: DefaultChartOptions = new DefaultChartOptions();

  xValues: number[] = [];

  yMaxValues: number[] = [];

  yMinValues: number[] = [];

  dependentVariables: string[] = [];

  selectedSetName = '';

  get variableSets(): {
    name: string;
    indices: number[];
    points: number[];
    maxs: number[];
    mins: number[];
  }[] {
    const uniqueVariables = [...new Set(this.dependentVariables)];
    const sets = uniqueVariables.map((name) => {
      const indices: number[] = [];
      const points: number[] = [];
      const mins: number[] = [];
      const maxs: number[] = [];

      return {
        name,
        indices,
        points,
        mins,
        maxs,
      };
    });

    // group points and indices with sets
    this.xValues.forEach((x, i) => {
      const currentSet = this.dependentVariables ? this.dependentVariables[i] : undefined;
      if (currentSet !== undefined) {
        const setIndex = sets.map((set) => set.name).indexOf(currentSet);
        sets[setIndex].points.push(x);
        sets[setIndex].indices.push(i);
        sets[setIndex].mins.push(this.yMinValues[i]);
        sets[setIndex].maxs.push(this.yMaxValues[i]);
      }
    });

    return sets;
  }

  get baselineSets(): {
    name: string;
    indices: number[];
    points: number[];
    maxs: number[];
    mins: number[];
  }[] {
    const uniqueVariables = [...new Set(this.baseline.dependentVariable)];
    const sets = uniqueVariables.map((name) => {
      const indices: number[] = [];
      const points: number[] = [];
      const mins: number[] = [];
      const maxs: number[] = [];

      return {
        name,
        indices,
        points,
        mins,
        maxs,
      };
    });

    // group points and indices with sets
    if (this.baseline.xValues !== undefined) {
      this.baseline.xValues.forEach((x, i) => {
        const currentSet = this.baseline.dependentVariable ? this.baseline.dependentVariable[i] : undefined;
        if (
          currentSet !== undefined &&
          this.baseline.yMinimumValues !== undefined &&
          this.baseline.yMaximumValues !== undefined
        ) {
          const setIndex = sets.map((set) => set.name).indexOf(currentSet);
          sets[setIndex].points.push(x);
          sets[setIndex].indices.push(i);
          sets[setIndex].mins.push(this.baseline.yMinimumValues[i]);
          sets[setIndex].maxs.push(this.baseline.yMaximumValues[i]);
        }
      });
    }

    return sets;
  }

  get selectedSet(): {
    name: string;
    indices: number[];
    points: number[];
    maxs: number[];
    mins: number[];
  } {
    return this.variableSets.filter((set) => set.name === this.selectedSetName)[0];
  }

  get min(): number {
    return Math.min(...this.selectedSet.points);
  }

  get max(): number {
    return Math.max(...this.selectedSet.points);
  }

  get displayChart(): boolean {
    return this.selectedSet && this.yMinValues.length > 0 && this.yMaxValues.length > 0;
  }

  get chartData(): DefaultChartData {
    const dataSets: ScatterChartDataset[] = [];
    const colorProvider = new CycleColorProvider();
    const baselineColor = colorProvider.getNextColor();
    const currentColor = colorProvider.getNextColor();

    const baselineSet = this.baselineSets.filter((set) => set.name === this.selectedSetName)[0];

    const baselineMins: ChartPoint2D[] = baselineSet.points.map((x, i) => new ChartPoint2D(x, baselineSet.mins[i]));
    const baselineMaxs: ChartPoint2D[] = baselineSet.points.map((x, i) => new ChartPoint2D(x, baselineSet.maxs[i]));

    if (baselineMins.length) {
      // dataset label will be hidden in chart legend
      const baselineMinScatter = new ScatterChartDataset(baselineMins, 'Min', colorProvider, undefined, baselineColor);
      dataSets.push(baselineMinScatter);
    }

    if (baselineMaxs.length) {
      const baselineMaxScatter = new ScatterChartDataset(
        baselineMaxs,
        'Baseline',
        colorProvider,
        undefined,
        baselineColor,
      );
      baselineMaxScatter.fill = '-1';
      dataSets.push(baselineMaxScatter);
    }

    const selectedXValues = this.selectedSet.points.sort((a, b) => a - b);

    const currentMins: ChartPoint2D[] = selectedXValues.map((x, i) => new ChartPoint2D(x, this.selectedSet.mins[i]));
    const currentMaxs: ChartPoint2D[] = selectedXValues.map((x, i) => new ChartPoint2D(x, this.selectedSet.maxs[i]));

    if (currentMins.length) {
      // dataset label will be hidden in chart legend
      const minScatter = new ScatterChartDataset(currentMins, 'Min', colorProvider, undefined, currentColor);
      dataSets.push(minScatter);
    }

    if (currentMaxs.length) {
      const maxScatter = new ScatterChartDataset(currentMaxs, 'Current', colorProvider, undefined, currentColor);
      maxScatter.fill = '-1';
      dataSets.push(maxScatter);
    }

    return new DefaultChartData(dataSets);
  }

  @Watch('parameterValue')
  onParameterChanged(): void {
    this.setValues();
  }

  @Watch('selectedSetName')
  onSelectedSetChanged(): void {
    this.editPoint = false;
  }

  addPoint(): void {
    if (this.selectedSet.points.length >= 6) {
      return;
    }
    // Insert new point at median of existing points
    const index = Math.floor(this.selectedSet.points.length / 2);

    // Choose point halfway between median points
    const point = (this.selectedSet.points[index - 1] + this.selectedSet.points[index]) / 2;

    // Interpolate to choose efficacy
    const minEfficacy = (this.selectedSet.mins[index - 1] + this.selectedSet.mins[index]) / 2;
    const maxEfficacy = (this.selectedSet.maxs[index - 1] + this.selectedSet.maxs[index]) / 2;

    this.dependentVariables.splice(this.selectedSet.indices[index], 0, this.selectedSetName);
    this.xValues.splice(this.selectedSet.indices[index], 0, point);
    this.yMinValues.splice(this.selectedSet.indices[index], 0, minEfficacy);
    this.yMaxValues.splice(this.selectedSet.indices[index], 0, maxEfficacy);
  }

  removePoint(index: number): void {
    if (this.selectedSet.points.length <= 2) {
      return;
    }

    // Remove point
    this.dependentVariables.splice(index, 1);
    this.xValues.splice(index, 1);
    this.yMinValues.splice(index, 1);
    this.yMaxValues.splice(index, 1);

    this.selectedIndex = -1;
    this.editPoint = false;
  }

  updateOnTextChange(value: string, maxOrMin: string, index: number): void {
    if (index === -1) {
      return;
    }

    const newValue = Number(value);
    if (maxOrMin === 'max') {
      this.yMaxValues.splice(index, 1, newValue);
    } else if (maxOrMin === 'min') {
      this.yMinValues.splice(index, 1, newValue);
    }
  }

  validationRulesMin(value: number): boolean | string {
    if (value > this.yMaxValues[this.selectedSet.indices[this.selectedIndex]]) {
      return `Value must be less than or equal to max: ${
        this.yMaxValues[this.selectedSet.indices[this.selectedIndex]]
      }`;
    }
    return true;
  }

  validationRulesMax(value: number): boolean | string {
    if (value < this.yMinValues[this.selectedSet.indices[this.selectedIndex]]) {
      return `Value must be greater than or equal to min: ${
        this.yMinValues[this.selectedSet.indices[this.selectedIndex]]
      }`;
    }
    return true;
  }

  // eslint-disable-next-line @typescript-eslint/no-explicit-any
  onHover(event: MouseEvent, elements: any[]): void {
    if (elements.length !== 0) {
      // eslint-disable-next-line no-underscore-dangle
      this.selectedIndex = elements[0]._index;
    }
  }

  // eslint-disable-next-line @typescript-eslint/no-explicit-any
  onClick(event: MouseEvent, elements: any[]): void {
    if (elements.length === 0) {
      this.selectedIndex = -1;
    }
    this.editPoint = this.selectedIndex >= 0;
  }

  // adapted from mawir's answer on Stack Overflow: https://stackoverflow.com/a/59716739
  // eslint-disable-next-line class-methods-use-this
  legendOnClick(event: MouseEvent, legendItem: ChartLegendLabelItem): void {
    const index = legendItem.datasetIndex;
    if (index !== undefined) {
      // get last instance of chart
      const chart = Object.values(Chart.instances)[Object.keys(Chart.instances).length - 1];
      const maxMeta = chart.getDatasetMeta(index);
      const minMeta = chart.getDatasetMeta(index - 1);

      minMeta.hidden = !minMeta.hidden;
      maxMeta.hidden = !maxMeta.hidden;

      chart.update();
    }
  }

  vuetifyColorProps(): unknown {
    return {
      '--primary-color': this.$vuetify.theme.currentTheme.primary,
    };
  }

  setValues(): void {
    if (this.key) {
      // get baseline
      this.baseline = this.$store.state.currentSelectedParameter.baseline.values[this.key];
    }
    this.xValues = this.parameterValue.xValues ?? [];
    this.yMinValues = this.parameterValue.yMinimumValues ?? [];
    this.yMaxValues = this.parameterValue.yMaximumValues ?? [];
    this.dependentVariables = this.parameterValue.dependentVariable ?? [];

    // update chart legend
    if (this.chartOptions.legend.labels !== undefined) {
      // hide min labels
      this.chartOptions.legend.labels.filter = (item) => !item.text?.includes('Min');

      // group baseline and current datasets onclick
      this.chartOptions.legend.onClick = this.legendOnClick;
    }

    // set chart event callbacks
    this.chartOptions.onClick = this.onClick;
    this.chartOptions.onHover = this.onHover;

    this.selectedSetName = this.variableSets[0].name;
  }

  created(): void {
    this.setValues();
  }
}
</script>

<style scoped lang="scss"></style>
