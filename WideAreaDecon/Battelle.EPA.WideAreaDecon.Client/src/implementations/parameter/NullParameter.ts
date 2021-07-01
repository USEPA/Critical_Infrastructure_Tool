import ParameterType from '@/enums/parameter/parameterType';
import IParameter from '@/interfaces/parameter/IParameter';
import { JsonProperty, Serializable } from 'typescript-json-serializer';
import ParameterMetaData from './ParameterMetaData';

@Serializable()
export default class NullParameter implements IParameter {
  @JsonProperty()
  metaData: ParameterMetaData = new ParameterMetaData();

  type = ParameterType.null;

  // eslint-disable-next-line class-methods-use-this
  get isSet(): boolean {
    return false;
  }

  isEquivalent(other: IParameter): boolean {
    if (other.type !== this.type) {
      return false;
    }
    return true;
  }
}
