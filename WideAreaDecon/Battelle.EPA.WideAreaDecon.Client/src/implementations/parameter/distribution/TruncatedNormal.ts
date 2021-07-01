import { JsonProperty, Serializable } from 'typescript-json-serializer';
import Distribution, { TruncatedNormalDistribution } from 'battelle-common-typescript-statistics';
import ParameterType from '@/enums/parameter/parameterType';
import IParameter from '@/interfaces/parameter/IParameter';
import IUnivariateParameter from '@/interfaces/parameter/IUnivariateParameter';
import ParameterMetaData from '../ParameterMetaData';

@Serializable()
export default class TruncatedNormal implements IUnivariateParameter {
  @JsonProperty()
  readonly type: ParameterType = ParameterType.truncatedNormal;

  @JsonProperty()
  min?: number;

  @JsonProperty()
  max?: number;

  @JsonProperty()
  mean?: number;

  public get mode(): number | undefined {
    return this.mean;
  }

  @JsonProperty()
  stdDev?: number;

  @JsonProperty()
  metaData: ParameterMetaData;

  public get isSet(): boolean {
    return this.min !== undefined && this.max !== undefined && this.mean !== undefined && this.stdDev !== undefined;
  }

  constructor(metaData = new ParameterMetaData(), min?: number, max?: number, mean?: number, stdDev?: number) {
    this.min = min;
    this.max = max;
    this.mean = mean;
    this.stdDev = stdDev;
    this.metaData = metaData;
  }

  get distribution(): Distribution | undefined {
    if (this.min === undefined || this.max === undefined || this.mean === undefined || this.stdDev === undefined) {
      return undefined;
    }
    return new TruncatedNormalDistribution(this.mean, this.stdDev, this.min, this.max);
  }

  isEquivalent(other: IParameter): boolean {
    return this.compareValues(other as TruncatedNormal);
  }

  compareValues(other?: TruncatedNormal): boolean {
    return other
      ? this.type === other.type &&
          this.min === other.min &&
          this.max === other.max &&
          this.mean === other.mean &&
          this.stdDev === other.stdDev
      : false;
  }
}
