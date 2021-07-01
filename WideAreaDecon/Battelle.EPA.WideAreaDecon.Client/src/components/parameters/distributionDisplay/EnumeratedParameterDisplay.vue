<template>
  <v-container>
    <v-row>
      <v-col><v-spacer /></v-col>
    </v-row>
    <v-row>
      <v-col cols="3">
        <v-overflow-btn
          @change="onDistributionTypeChange"
          class="my-2"
          v-model="currentDistType"
          :items="distNames"
          filled
          dense
        >
          <template v-slot:prepend>
            <p>Distribution:</p>
          </template>
        </v-overflow-btn>
      </v-col>
      <v-col offset="5" cols="3">
        <v-overflow-btn
          @change="onCategoryChanged"
          class="my-2"
          :items="categories"
          :item-text="[0]"
          :item-value="[1]"
          v-model="selectedCategory"
          filled
          dense
          ref="categorySelect"
        >
          <template v-slot:prepend>
            <p>Category:</p>
          </template>
          <template v-slot:item="{ item, attrs, on }">
            <v-list-item :class="getClass(item[0])" v-bind="attrs" v-on="on">
              <v-list-item-content>
                <v-list-item-title :id="attrs['aria-labelledby']" v-text="item[0]"></v-list-item-title>
              </v-list-item-content>
            </v-list-item>
          </template>
        </v-overflow-btn>
      </v-col>
    </v-row>
    <component :key="getSelectedCategoryName()" :is="display.distComponent" :parameter-value="selectedCategory">
    </component>
    <v-card v-if="display.displayChart" flat class="pa-5" tile width="100%" height="400">
      <distribution-chart
        :distribution-series="display.chartData"
        :xAxisLabel="display.xAxisLabel"
        :yAxisLabel="'Probability of Selection'"
        :data-generator="display.dataGenerator"
      ></distribution-chart>
    </v-card>
  </v-container>
</template>

<script lang="ts">
import Vue from 'vue';
import { Component, Prop, Watch } from 'vue-property-decorator';
import IParameterDisplay from '@/interfaces/component/IParameterDisplay';
import IParameter from '@/interfaces/parameter/IParameter';
import EnumeratedParameter from '@/implementations/parameter/list/enumeratedParameter';
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
import WeibullDisplay from '@/components/parameters/distributionDisplay/WeibullDisplay.vue';
import BimodalTruncatedNormalDisplay from '@/components/parameters/distributionDisplay/BimodalTruncatedNormalDisplay.vue';
import UniformXDependentDisplay from '@/components/parameters/distributionDisplay/UniformXDependentDisplay.vue';
import { DistributionChart } from 'battelle-common-vue-charting/src/index';
import { changeableDistributionTypes } from '@/mixin/parameterMixin';
import container from '@/dependencyInjection/config';
import IParameterConverter from '@/interfaces/parameter/IParameterConverter';
import TYPES from '@/dependencyInjection/types';
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
    UniformDisplay,
    LogNormalDisplay,
    WeibullDisplay,
    BimodalTruncatedNormalDisplay,
    UniformXDependentDisplay,
    DistributionChart,
  },
})
export default class EnumeratedParameterDisplay extends Vue implements IParameterDisplay {
  @Prop({ required: true }) parameterValue!: EnumeratedParameter;

  baseline: EnumeratedParameter = this.$store.state.currentSelectedParameter.baseline;

  selectedCategory: IParameter = Object.values(this.parameterValue.values)[0];

  // baseline value of selected category
  baselineCategory: IParameter = Object.values(this.baseline.values)[0];

  currentDistType: ParameterType = ParameterType.constant;

  distNames: ParameterType[] = changeableDistributionTypes;

  parameterConverter = container.get<IParameterConverter>(TYPES.ParameterConverter);

  get display(): DistributionDisplay {
    return container
      .get<IDistributionDisplayProvider>(TYPES.DistributionDisplayProvider)
      .getDistributionDisplay(this.baselineCategory, this.selectedCategory);
  }

  get categories(): [string, IParameter][] {
    return Object.entries(this.parameterValue.values);
  }

  onCategoryChanged(): void {
    this.currentDistType = this.selectedCategory.type ?? ParameterType.constant;

    const category = this.getSelectedCategoryName();
    this.baselineCategory = this.baseline.values[category];
  }

  onDistributionTypeChange(): void {
    const category = this.getSelectedCategoryName();
    this.selectedCategory = this.parameterConverter.convertToNewType(this.selectedCategory, this.currentDistType);

    this.parameterValue.values[category] = this.selectedCategory;
  }

  getSelectedCategoryName(): string {
    const values = this.categories;
    const [[category]] = values.filter(([, value]) => value === this.selectedCategory);

    return category;
  }

  getClass(cateogry: string): string {
    const param = this.parameterValue.values[cateogry];
    if (param.isSet === undefined) {
      return '';
    }
    return param.isSet ? '' : `error lighten-2`;
  }

  @Watch('selectedCategory', { deep: true })
  checkErrorHighligtingOnSelect(): void {
    if (this.selectedCategory.isSet === undefined) {
      return;
    }

    const el = (this.$refs.categorySelect as Vue).$el.children[1].children[0];
    const errorClasses = ['error', 'lighten-2'];

    if (this.selectedCategory.isSet) {
      el.classList.remove(...errorClasses);
    } else {
      el.classList.add(...errorClasses);
    }
  }

  @Watch('parameterValue')
  onParameterChanged(): void {
    // update selected category, current dist type, and baseline values
    [[, this.selectedCategory]] = this.categories;
    this.currentDistType = this.selectedCategory.type ?? ParameterType.constant;

    this.baseline = this.$store.state.currentSelectedParameter.baseline;
    [this.baselineCategory] = Object.values(this.baseline.values);
  }

  created(): void {
    this.currentDistType = this.selectedCategory.type;
  }

  mounted(): void {
    this.checkErrorHighligtingOnSelect();
  }
}
</script>

<style scoped lang="scss">
.v-list-item--active.error {
  color: var(--v-primary-base) !important;
}
</style>
