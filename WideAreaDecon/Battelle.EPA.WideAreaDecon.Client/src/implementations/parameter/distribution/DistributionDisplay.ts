import Distribution, { DistributionDataGenerator } from 'battelle-common-typescript-statistics';
import IUnivariateParameter from '@/interfaces/parameter/IUnivariateParameter';
import ParameterType from '@/enums/parameter/parameterType';
import IParameter from '@/interfaces/parameter/IParameter';

export default class DistributionDisplay {
  baseline: IUnivariateParameter;

  current: IUnivariateParameter;

  get chartData(): Distribution[] {
    const distributions: Distribution[] = [];

    if (this.baseline.distribution !== undefined) {
      distributions.push(this.baseline.distribution);
    }

    if (this.current.distribution !== undefined) {
      distributions.push(this.current.distribution);
    }

    return distributions;
  }

  get displayChart(): boolean {
    switch (this.current.type) {
      case ParameterType.uniform:
      case ParameterType.pert:
      case ParameterType.truncatedNormal:
      case ParameterType.bimodalTruncatedNormal:
      case ParameterType.logUniform:
      case ParameterType.truncatedLogNormal:
      case ParameterType.logNormal:
      case ParameterType.weibull:
        return this.chartData.length > 0;
      case ParameterType.constant:
      case ParameterType.enumeratedFraction:
      case ParameterType.enumeratedParameter:
      case ParameterType.uniformXDependent:
      case ParameterType.null:
      default:
        return false;
    }
  }

  get dataGenerator(): DistributionDataGenerator {
    let min = this.baseline.metaData.lowerLimit;
    let max = this.baseline.metaData.upperLimit;

    if (this.current.min !== undefined && this.baseline.min !== undefined) {
      min = this.current.min < this.baseline.min ? this.current.min : this.baseline.min;
    }

    if (this.current.max !== undefined && this.baseline.max !== undefined) {
      max = this.current.max > this.baseline.max ? this.current.max : this.baseline.max;
    }

    const gen = new DistributionDataGenerator(1000, min, max);
    return gen;
  }

  get distComponent(): string {
    switch (this.current.type) {
      case ParameterType.null:
        return 'null-display';
      case ParameterType.constant:
        return 'constant-display';
      case ParameterType.logUniform:
        return 'log-uniform-display';
      case ParameterType.pert:
        return 'beta-pert-display';
      case ParameterType.truncatedLogNormal:
        return 'truncated-log-normal-display';
      case ParameterType.truncatedNormal:
        return 'truncated-normal-display';
      case ParameterType.logNormal:
        return 'log-normal-display';
      case ParameterType.uniform:
        return 'uniform-display';
      case ParameterType.uniformXDependent:
        return 'uniform-x-dependent-display';
      case ParameterType.weibull:
        return 'weibull-display';
      case ParameterType.bimodalTruncatedNormal:
        return 'bimodal-truncated-normal-display';
      case ParameterType.enumeratedFraction:
        return 'enumerated-fraction-display';
      case ParameterType.enumeratedParameter:
        return 'enumerated-parameter-display';
      default:
        return 'unknown-display';
    }
  }

  get xAxisLabel(): string {
    return `${this.baseline.metaData.description} (${this.baseline.metaData.units})` ?? '';
  }

  constructor(baseline: IParameter, current: IParameter) {
    this.baseline = baseline as IUnivariateParameter;
    this.current = current as IUnivariateParameter;
  }
}
