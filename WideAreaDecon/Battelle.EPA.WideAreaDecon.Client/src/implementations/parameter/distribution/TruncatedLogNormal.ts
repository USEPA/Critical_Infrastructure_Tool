import { JsonProperty, Serializable } from 'typescript-json-serializer';
import Distribution, { TruncatedLogNormalDistribution } from 'battelle-common-typescript-statistics';
import ParameterType from '@/enums/parameter/parameterType';
import IParameter from '@/interfaces/parameter/IParameter';
import IUnivariateParameter from '@/interfaces/parameter/IUnivariateParameter';
import ParameterMetaData from '../ParameterMetaData';

@Serializable()
export default class TruncatedLogNormal implements IUnivariateParameter {
  @JsonProperty()
  readonly type: ParameterType = ParameterType.truncatedLogNormal;

  @JsonProperty()
  logMin?: number;

  @JsonProperty()
  logMax?: number;

  @JsonProperty()
  logMean?: number;

  @JsonProperty()
  logStdDev?: number;

  get min(): number | undefined {
    return this.logMin !== undefined ? 10 ** this.logMin : undefined;
  }

  get max(): number | undefined {
    return this.logMax !== undefined ? 10 ** this.logMax : undefined;
  }

  get mean(): number | undefined {
    return this.logMean !== undefined ? 10 ** this.logMean : undefined;
  }

  get mode(): number | undefined {
    return this.mean; // TODO: how to calculate
  }

  get stdDev(): number | undefined {
    return this.logStdDev !== undefined ? 10 ** this.logStdDev : undefined;
  }

  @JsonProperty()
  metaData: ParameterMetaData;

  public get isSet(): boolean {
    return (
      this.logMin !== undefined &&
      this.logMax !== undefined &&
      this.logMean !== undefined &&
      this.logStdDev !== undefined
    );
  }

  constructor(
    metaData = new ParameterMetaData(),
    logMin?: number,
    logMax?: number,
    logMean?: number,
    logStdDev?: number,
  ) {
    this.logMin = logMin;
    this.logMax = logMax;
    this.logMean = logMean;
    this.logStdDev = logStdDev;
    this.metaData = metaData;
  }

  isEquivalent(other: IParameter): boolean {
    return this.compareValues(other as TruncatedLogNormal);
  }

  compareValues(other?: TruncatedLogNormal): boolean {
    return other
      ? this.type === other.type &&
          this.logMin === other.logMin &&
          this.logMax === other.logMax &&
          this.logMean === other.logMean &&
          this.logStdDev === other.logStdDev
      : false;
  }

  get distribution(): Distribution | undefined {
    if (
      this.min === undefined ||
      this.max === undefined ||
      this.logMean === undefined ||
      this.logStdDev === undefined
    ) {
      return undefined;
    }
    return new TruncatedLogNormalDistribution(this.logMean, this.logStdDev, this.min, this.max);
  }
}
