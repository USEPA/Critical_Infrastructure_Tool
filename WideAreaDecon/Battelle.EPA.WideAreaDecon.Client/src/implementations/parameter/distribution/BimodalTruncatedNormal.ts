import { JsonProperty, Serializable } from 'typescript-json-serializer';
import ParameterType from '@/enums/parameter/parameterType';
import IParameter from '@/interfaces/parameter/IParameter';
import IUnivariateParameter from '@/interfaces/parameter/IUnivariateParameter';
import Distribution, { BimodalTruncatedNormalDistribution } from 'battelle-common-typescript-statistics';
import ParameterMetaData from '../ParameterMetaData';

@Serializable()
export default class BimodalTruncatedNormal implements IUnivariateParameter {
  @JsonProperty()
  readonly type: ParameterType = ParameterType.bimodalTruncatedNormal;

  @JsonProperty()
  mean1?: number;

  @JsonProperty()
  stdDev1?: number;

  @JsonProperty()
  mean2?: number;

  @JsonProperty()
  stdDev2?: number;

  @JsonProperty()
  min?: number;

  @JsonProperty()
  max?: number;

  get mean(): number | undefined {
    if (
      !(
        this.mean1 !== undefined &&
        this.stdDev1 !== undefined &&
        this.mean2 !== undefined &&
        this.stdDev2 !== undefined &&
        this.min !== undefined &&
        this.max !== undefined
      )
    ) {
      return undefined;
    }
    return (this.mean1 + this.mean2) / 2.0;
  }

  get stdDev(): number | undefined {
    if (
      !(
        this.mean1 !== undefined &&
        this.stdDev1 !== undefined &&
        this.mean2 !== undefined &&
        this.stdDev2 !== undefined &&
        this.min !== undefined &&
        this.max !== undefined
      )
    ) {
      return undefined;
    }
    return (this.max - this.min) / 6.0;
  }

  @JsonProperty()
  metaData: ParameterMetaData;

  public get isSet(): boolean {
    return (
      this.mean1 !== undefined &&
      this.stdDev1 !== undefined &&
      this.mean2 !== undefined &&
      this.stdDev2 !== undefined &&
      this.min !== undefined &&
      this.max !== undefined
    );
  }

  constructor(
    metaData = new ParameterMetaData(),
    mean1?: number,
    stdDev1?: number,
    mean2?: number,
    stdDev2?: number,
    min?: number,
    max?: number,
  ) {
    this.mean1 = mean1;
    this.stdDev1 = stdDev1;
    this.mean2 = mean2;
    this.stdDev2 = stdDev2;
    this.min = min;
    this.max = max;
    this.metaData = metaData;
  }

  get distribution(): Distribution | undefined {
    if (
      this.min === undefined ||
      this.max === undefined ||
      this.mean1 === undefined ||
      this.stdDev1 === undefined ||
      this.mean2 === undefined ||
      this.stdDev2 === undefined
    ) {
      return undefined;
    }
    return new BimodalTruncatedNormalDistribution(
      this.mean1,
      this.stdDev1,
      this.mean2,
      this.stdDev2,
      this.min,
      this.max,
    );
  }

  isEquivalent(other: IParameter): boolean {
    return this.compareValues(other as BimodalTruncatedNormal);
  }

  compareValues(other?: BimodalTruncatedNormal): boolean {
    return other
      ? this.type === other.type &&
          this.min === other.min &&
          this.max === other.max &&
          this.mean1 === other.mean1 &&
          this.mean2 === other.mean2 &&
          this.stdDev1 === other.stdDev1 &&
          this.stdDev2 === other.stdDev2
      : false;
  }
}
