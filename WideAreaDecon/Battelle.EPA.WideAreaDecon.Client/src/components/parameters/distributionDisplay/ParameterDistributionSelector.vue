<template>
  <v-card height="100%" width="100%">
    <v-row dense>
      <v-col cols="auto" class="mr-auto">
        <v-card-title v-if="shouldIncludeTitle" v-text="currentSelectedParameter.path" />
      </v-col>
      <v-col align-self="center" cols="3">
        <v-overflow-btn
          v-if="isChangeableDist"
          @change="onDistributionTypeChange"
          class="my-2"
          v-model="currentDistType"
          :items="distNames"
          filled
          dense
        />
      </v-col>
      <v-col style="margin-top: 7px" cols="2">
        <v-btn height="45" v-if="shouldIncludeTitle && parameterHasChanged" color="secondary" @click="resetParameter">
          Reset Parameter
        </v-btn>
      </v-col>
    </v-row>
    <v-divider color="grey" v-if="shouldIncludeTitle"></v-divider>
    <component
      :key="currentSelectedParameter.path"
      :is="display.distComponent"
      :parameter-value="currentSelectedParameter.current"
    >
    </component>
    <v-container>
      <v-card v-if="display.displayChart" flat class="pa-5" tile width="100%" height="400">
        <distribution-chart
          :distribution-series="display.chartData"
          :xAxisLabel="display.xAxisLabel"
          :yAxisLabel="'Probability of Selection'"
          :data-generator="display.dataGenerator"
        ></distribution-chart>
      </v-card>
    </v-container>
  </v-card>
</template>

<script lang="ts">
import Vue from 'vue';
import { Component, Watch } from 'vue-property-decorator';
import { Action, Getter, State } from 'vuex-class';
import ParameterType from '@/enums/parameter/parameterType';
import NullDisplay from '@/components/parameters/distributionDisplay/NullDisplay.vue';
import UnknownDisplay from '@/components/parameters/distributionDisplay/UnknownDisplay.vue';
import ConstantDisplay from '@/components/parameters/distributionDisplay/ConstantDisplay.vue';
import LogUniformDisplay from '@/components/parameters/distributionDisplay/LogUniformDisplay.vue';
import BetaPertDisplay from '@/components/parameters/distributionDisplay/BetaPertDisplay.vue';
import TruncatedLogNormalDisplay from '@/components/parameters/distributionDisplay/TruncatedLogNormalDisplay.vue';
import TruncatedNormalDisplay from '@/components/parameters/distributionDisplay/TruncatedNormalDisplay.vue';
import LogNormalDisplay from '@/components/parameters/distributionDisplay/LogNormalDisplay.vue';
import UniformDisplay from '@/components/parameters/distributionDisplay/UniformDisplay.vue';
import UniformXDependentDisplay from '@/components/parameters/distributionDisplay/UniformXDependentDisplay.vue';
import WeibullDisplay from '@/components/parameters/distributionDisplay/WeibullDisplay.vue';
import BimodalTruncatedNormalDisplay from '@/components/parameters/distributionDisplay/BimodalTruncatedNormalDisplay.vue';
import EnumeratedFractionDisplay from '@/components/parameters/distributionDisplay/EnumeratedFractionDisplay.vue';
import EnumeratedParameterDisplay from '@/components/parameters/distributionDisplay/EnumeratedParameterDisplay.vue';
import ParameterWrapper from '@/implementations/parameter/ParameterWrapper';
import { changeableDistributionTypes } from '@/mixin/parameterMixin';
import container from '@/dependencyInjection/config';
import IParameterConverter from '@/interfaces/parameter/IParameterConverter';
import TYPES from '@/dependencyInjection/types';
import { DistributionChart } from 'battelle-common-vue-charting/src/index';
import DistributionDisplay from '@/implementations/parameter/distribution/DistributionDisplay';
import IDistributionDisplayProvider from '@/interfaces/providers/IDistributionDisplayProvider';

@Component({
  components: {
    NullDisplay,
    UnknownDisplay,
    ConstantDisplay,
    LogUniformDisplay,
    BetaPertDisplay,
    TruncatedLogNormalDisplay,
    TruncatedNormalDisplay,
    UniformXDependentDisplay,
    UniformDisplay,
    LogNormalDisplay,
    WeibullDisplay,
    BimodalTruncatedNormalDisplay,
    EnumeratedFractionDisplay,
    EnumeratedParameterDisplay,
    DistributionChart,
  },
})
export default class ParameterDistributionSelector extends Vue {
  @State currentSelectedParameter!: ParameterWrapper;

  @Getter hasResults!: boolean;

  @Action resetCurrentJobRequest!: () => void;

  parameterConverter = container.get<IParameterConverter>(TYPES.ParameterConverter);

  @Watch('currentSelectedParameter')
  onCurrentSelectedParameterChange(): void {
    this.currentDistType = this.currentSelectedParameter.type;
  }

  @Watch('parameterHasChanged')
  onParameterChanged(newValue: boolean): void {
    if (newValue && this.hasResults) {
      this.resetCurrentJobRequest();
    }
  }

  currentDistType = ParameterType.constant;

  distNames = changeableDistributionTypes;

  get display(): DistributionDisplay {
    return container
      .get<IDistributionDisplayProvider>(TYPES.DistributionDisplayProvider)
      .getDistributionDisplay(this.currentSelectedParameter.baseline, this.currentSelectedParameter.current);
  }

  get isChangeableDist(): boolean {
    return changeableDistributionTypes.find((p) => p === this.currentSelectedParameter.type) !== undefined;
  }

  get shouldIncludeTitle(): boolean {
    return this.currentSelectedParameter.type !== ParameterType.null;
  }

  get parameterHasChanged(): boolean {
    return this.currentSelectedParameter.isChanged();
  }

  resetParameter(): void {
    this.$store.commit('resetCurrentSelectedParameter');
    this.currentDistType = this.currentSelectedParameter.type;
  }

  onDistributionTypeChange(): void {
    this.$store.commit(
      'changeCurrentParameterType',
      this.parameterConverter.convertToNewType(this.currentSelectedParameter.current, this.currentDistType),
    );
  }

  created(): void {
    this.currentDistType = this.currentSelectedParameter.type;
  }
}
</script>

<style scoped lang="scss"></style>
