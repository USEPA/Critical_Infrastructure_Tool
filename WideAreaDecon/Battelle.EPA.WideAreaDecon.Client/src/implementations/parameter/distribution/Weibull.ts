import { JsonProperty, Serializable } from 'typescript-json-serializer';
import ParameterType from '@/enums/parameter/parameterType';
import Distribution, { WeibullDistribution } from 'battelle-common-typescript-statistics';
import * as Utility from '@/mixin/mathUtilityMixin';
import IUnivariateParameter from '@/interfaces/parameter/IUnivariateParameter';
import ParameterMetaData from '../ParameterMetaData';

@Serializable()
export default class Weibull implements IUnivariateParameter {
  @JsonProperty()
  readonly type = ParameterType.weibull;

  @JsonProperty()
  k?: number;

  @JsonProperty()
  lambda?: number;

  get min(): number {
    return this.metaData.lowerLimit;
  }

  get max(): number {
    return this.metaData.lowerLimit;
  }

  // What is the difference between calculateMean and the mean member getter
  static calculateMean(lambda: number, k: number): number {
    return lambda * Utility.gamma(1 + 1 / k);
  }

  get mean(): number | undefined {
    if (this.k === undefined || this.lambda === undefined) {
      return undefined;
    }
    return Weibull.calculateMean(this.lambda, this.k); // this.lambda * Utility.gamma(1 + 1 / this.k);
  }

  get mode(): number | undefined {
    if (this.k === undefined || this.lambda === undefined) {
      return undefined;
    }
    return this.k <= 1 ? 0 : this.lambda * ((this.k - 1) / this.k) ** (1 / this.k);
  }

  get stdDev(): number | undefined {
    if (!this.isSet) {
      return undefined;
    }
    return this.variance ? Math.sqrt(this.variance) : undefined;
  }

  get variance(): number | undefined {
    if (!(this.k !== undefined && this.lambda !== undefined)) {
      return undefined;
    }
    return this.lambda ** 2 * (Utility.gamma(1 + 2 / this.k) - Utility.gamma(1 + 1 / this.k) ** 2);
  }

  get isSet(): boolean {
    return this.k !== undefined && this.lambda !== undefined;
  }

  isEquivalent(other: Weibull): boolean {
    if (!(this.k !== undefined && this.lambda !== undefined && other.k !== undefined && other.lambda !== undefined)) {
      return false;
    }
    return this.k === other.k && this.lambda === other.lambda;
  }

  @JsonProperty()
  metaData: ParameterMetaData;

  constructor(metaData: ParameterMetaData = new ParameterMetaData(), k?: number, lambda?: number) {
    this.metaData = metaData;
    this.k = k;
    this.lambda = lambda;
  }

  get distribution(): Distribution | undefined {
    if (this.k === undefined || this.lambda === undefined) {
      return undefined;
    }
    return new WeibullDistribution(this.k, this.lambda);
  }
}
