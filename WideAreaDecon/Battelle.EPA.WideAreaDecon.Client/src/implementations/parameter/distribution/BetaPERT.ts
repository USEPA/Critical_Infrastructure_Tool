import { JsonProperty, Serializable } from 'typescript-json-serializer';
import Distribution, { PertDistribution } from 'battelle-common-typescript-statistics';
import ParameterType from '@/enums/parameter/parameterType';
import IParameter from '@/interfaces/parameter/IParameter';
import IUnivariateParameter from '@/interfaces/parameter/IUnivariateParameter';
import ParameterMetaData from '../ParameterMetaData';

@Serializable()
export default class BetaPERT implements IUnivariateParameter {
  @JsonProperty()
  readonly type: ParameterType = ParameterType.pert;

  @JsonProperty()
  min?: number;

  @JsonProperty()
  max?: number;

  get mean(): number | undefined {
    if (!(this.min !== undefined && this.max !== undefined && this.mode !== undefined)) {
      return undefined;
    }
    return (this.min + 4 * this.mode + this.max) / 6.0;
  }

  @JsonProperty()
  mode?: number;

  get stdDev(): number | undefined {
    if (!(this.min !== undefined && this.max !== undefined && this.mode !== undefined)) {
      return undefined;
    }
    return (this.max - this.min) / 6.0;
  }

  @JsonProperty()
  metaData: ParameterMetaData;

  public get isSet(): boolean {
    return this.min !== undefined && this.max !== undefined && this.mode !== undefined;
  }

  constructor(metaData = new ParameterMetaData(), min?: number, max?: number, mode?: number) {
    this.min = min;
    this.max = max;
    this.mode = mode;
    this.metaData = metaData;
  }

  get distribution(): Distribution | undefined {
    if (this.min === undefined || this.max === undefined || this.mode === undefined) {
      return undefined;
    }
    return new PertDistribution(this.mode, this.min, this.max);
  }

  isEquivalent(other: IParameter): boolean {
    return this.compareValues(other as BetaPERT);
  }

  compareValues(other?: BetaPERT): boolean {
    return other
      ? this.type === other.type && this.min === other.min && this.max === other.max && this.mode === other.mode
      : false;
  }
}
