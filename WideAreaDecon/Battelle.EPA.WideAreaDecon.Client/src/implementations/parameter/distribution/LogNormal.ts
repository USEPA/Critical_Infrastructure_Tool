import { JsonProperty, Serializable } from 'typescript-json-serializer';
import Distribution, { LogNormalDistribution } from 'battelle-common-typescript-statistics';
import ParameterType from '@/enums/parameter/parameterType';
import IParameter from '@/interfaces/parameter/IParameter';
import IUnivariateParameter from '@/interfaces/parameter/IUnivariateParameter';
import ParameterMetaData from '../ParameterMetaData';

@Serializable()
export default class LogNormal implements IUnivariateParameter {
  @JsonProperty()
  readonly type: ParameterType = ParameterType.logNormal;

  public get min(): number {
    return this.metaData.lowerLimit;
  }

  public get max(): number {
    return this.metaData.upperLimit;
  }

  @JsonProperty()
  mean?: number;

  get mode(): number | undefined {
    return this.mean; // TODO: how to calculate
  }

  @JsonProperty()
  stdDev?: number;

  @JsonProperty()
  metaData: ParameterMetaData;

  public get isSet(): boolean {
    return this.mean !== undefined && this.stdDev !== undefined;
  }

  public get distribution(): Distribution | undefined {
    if (this.mean === undefined || this.stdDev === undefined) {
      return undefined;
    }
    return new LogNormalDistribution(this.mean, this.stdDev);
  }

  constructor(metaData = new ParameterMetaData(), mean?: number, stdDev?: number) {
    this.mean = mean;
    this.stdDev = stdDev;
    this.metaData = metaData;
  }

  isEquivalent(other: IParameter): boolean {
    return this.compareValues(other as LogNormal);
  }

  compareValues(other?: LogNormal): boolean {
    return other ? this.type === other.type && this.mean === other.mean && this.stdDev === other.stdDev : false;
  }
}
