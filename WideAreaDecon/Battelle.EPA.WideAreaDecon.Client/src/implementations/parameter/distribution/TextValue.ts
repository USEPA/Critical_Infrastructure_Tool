import { JsonProperty, Serializable } from 'typescript-json-serializer';
import ParameterType from '@/enums/parameter/parameterType';
import IParameter from '@/interfaces/parameter/IParameter';
import IUnivariateParameter from '@/interfaces/parameter/IUnivariateParameter';
import ParameterMetaData from '../ParameterMetaData';

@Serializable()
export default class TextValue implements IUnivariateParameter {
  private readonly numStdDevs = 5;

  @JsonProperty()
  readonly type: ParameterType = ParameterType.textValue;

  @JsonProperty()
  metaData: ParameterMetaData;

  locked?: boolean;

  public get isSet(): boolean {
    return this.value !== 'null' || this.value !== undefined;
  }

  @JsonProperty()
  public value: string;

  public get textValue(): string {
    return this.value;
  }

  constructor(metaData = new ParameterMetaData(), value?: string) {
    this.value = value || 'null';
    this.metaData = metaData;
  }

  isEquivalent(other: IParameter): boolean {
    return this.compareValues(other as TextValue);
  }

  compareValues(other?: TextValue): boolean {
    return other ? this.type === other.type && this.value === other.value : false;
  }
}
