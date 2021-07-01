import { JsonProperty, Serializable } from 'typescript-json-serializer';
import Distribution, { UniformDistribution } from 'battelle-common-typescript-statistics';
import ParameterType from '@/enums/parameter/parameterType';
import IParameter from '@/interfaces/parameter/IParameter';
import IUnivariateParameter from '@/interfaces/parameter/IUnivariateParameter';
import ParameterMetaData from '../ParameterMetaData';

@Serializable()
export default class Uniform implements IUnivariateParameter {
  @JsonProperty()
  readonly type: ParameterType = ParameterType.uniform;

  @JsonProperty()
  min?: number;

  @JsonProperty()
  max?: number;

  get mean(): number | undefined {
    return !!this.min && !!this.max ? (this.min + this.max) / 2.0 : undefined;
  }

  get mode(): number | undefined {
    return this.mean;
  }

  get stdDev(): number | undefined {
    return this.min !== undefined && this.max !== undefined ? (this.max - this.min) / 6.0 : undefined;
  }

  @JsonProperty()
  metaData: ParameterMetaData;

  public get isSet(): boolean {
    return this.min !== undefined && this.max !== undefined;
  }

  constructor(metaData = new ParameterMetaData(), min?: number, max?: number) {
    this.min = min;
    this.max = max;
    this.metaData = metaData;
  }

  get distribution(): Distribution | undefined {
    if (this.min === undefined || this.max === undefined) {
      return undefined;
    }
    return new UniformDistribution(this.min, this.max);
  }

  isEquivalent(other: IParameter): boolean {
    return this.compareValues(other as Uniform);
  }

  compareValues(other?: Uniform): boolean {
    return other ? this.type === other.type && this.min === other.min && this.max === other.max : false;
  }
}
