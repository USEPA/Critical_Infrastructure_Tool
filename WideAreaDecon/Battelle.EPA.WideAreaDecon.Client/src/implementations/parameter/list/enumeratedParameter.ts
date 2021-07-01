import { JsonProperty, Serializable } from 'typescript-json-serializer';
import { isEqual } from 'lodash';
import ParameterType from '@/enums/parameter/parameterType';
import IParameter from '@/interfaces/parameter/IParameter';
import EnumeratedParameterDeserializer from '@/serialization/parameter/EnumeratedParameterDeserializer';
import ParameterMetaData from '../ParameterMetaData';

@Serializable()
export default class EnumeratedParameter implements IParameter {
  @JsonProperty()
  readonly type = ParameterType.enumeratedParameter;

  public get isSet(): boolean {
    const valueEntries = Object.values(this.values);

    const result = valueEntries.every((val: IParameter) => {
      return val.isSet;
    });

    return result;
  }

  isEquivalent(other: IParameter): boolean {
    return isEqual(this, other);
  }

  @JsonProperty()
  metaData: ParameterMetaData;

  @JsonProperty({ ...{ isDictionary: true }, ...EnumeratedParameterDeserializer })
  values: Record<string, IParameter>;

  @JsonProperty()
  typeName?: string;

  constructor(metaData = new ParameterMetaData(), typeName?: string, values?: Record<string, IParameter>) {
    this.metaData = metaData;
    this.typeName = typeName;
    this.values = values ?? {};
  }
}
