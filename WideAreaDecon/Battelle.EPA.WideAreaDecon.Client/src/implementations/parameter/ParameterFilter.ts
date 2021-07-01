import { JsonProperty, Serializable } from 'typescript-json-serializer';
import ParameterDeserializer from '@/serialization/parameter/ParameterDeserializer';
import IParameter from '@/interfaces/parameter/IParameter';
import IParameterNode from '@/interfaces/parameter/IParameterNode';
import ParameterWrapperFilter from './ParameterWrapperFilter';
import ParameterWrapper from './ParameterWrapper';

@Serializable()
export default class ParameterFilter {
  @JsonProperty()
  name: string;

  @JsonProperty({
    predicate: () => {
      return ParameterFilter;
    },
  })
  public filters: Array<ParameterFilter>;

  @JsonProperty(ParameterDeserializer)
  public parameters: Array<IParameter>;

  constructor(name = 'unknown', filters?: ParameterFilter[], parameters?: IParameter[]) {
    this.name = name;
    this.filters = filters !== undefined ? filters : new Array<ParameterFilter>();
    this.parameters = parameters !== undefined ? parameters : new Array<IParameter>();
  }

  public toParameterWrapperFilter(parent: IParameterNode | null): ParameterWrapperFilter {
    const newFilter = new ParameterWrapperFilter(parent, this.name);

    newFilter.filters = this.filters.map((f) => f.toParameterWrapperFilter(newFilter));
    newFilter.parameters = this.parameters.map((p) => new ParameterWrapper(newFilter, p));

    return newFilter;
  }

  public allParametersValid(): boolean {
    return this.filters.every((f) => f.allParametersValid()) && this.parameters.every((p) => p.isSet);
  }

  public numberInvalidParameters(): number {
    let sum = 0;
    this.filters.forEach((f) => {
      sum += f.numberInvalidParameters();
    });
    this.parameters.forEach((p) => {
      sum += p.isSet ? 0 : 1;
    });
    return sum;
  }

  public subItemSelected(item: IParameter): boolean {
    return this.filters.some((f) => f.subItemSelected(item)) || this.parameters.some((p) => p === item);
  }
}
