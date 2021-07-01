import { JsonProperty, Serializable } from 'typescript-json-serializer';
import ParameterType from '@/enums/parameter/parameterType';
import IParameter from '@/interfaces/parameter/IParameter';
import IUnivariateParameter from '@/interfaces/parameter/IUnivariateParameter';
import ParameterMetaData from '../ParameterMetaData';

@Serializable()
export default class Constant implements IUnivariateParameter {
  private readonly numStdDevs = 5;

  @JsonProperty()
  readonly type: ParameterType = ParameterType.constant;

  @JsonProperty()
  metaData: ParameterMetaData;

  locked?: boolean;

  public get isSet(): boolean {
    return this.value !== undefined;
  }

  @JsonProperty()
  public value?: number;

  public get min(): number {
    return this.metaData.lowerLimit;
  }

  public get max(): number {
    return this.metaData.upperLimit;
  }

  public get mean(): number | undefined {
    return this.value;
  }

  public get mode(): number | undefined {
    return this.value;
  }

  public get stdDev(): number {
    return (this.metaData.upperLimit - this.metaData.lowerLimit) / this.numStdDevs;
  }

  constructor(metaData = new ParameterMetaData(), value?: number) {
    this.value = value;
    this.metaData = metaData;
  }

  isEquivalent(other: IParameter): boolean {
    return this.compareValues(other as Constant);
  }

  compareValues(other?: Constant): boolean {
    return other ? this.type === other.type && this.value === other.value : false;
  }
}
