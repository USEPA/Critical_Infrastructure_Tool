import { JsonProperty, Serializable } from 'typescript-json-serializer';
import ParameterWrapperFilter from './ParameterWrapperFilter';

@Serializable()
export default class ParameterWrapperList {
  @JsonProperty()
  version: number;

  @JsonProperty({
    predicate: () => ParameterWrapperFilter,
  })
  filters: Array<ParameterWrapperFilter>;

  constructor(version = 0, filters?: ParameterWrapperFilter[]) {
    this.version = version;
    this.filters = filters !== undefined ? filters : new Array<ParameterWrapperFilter>();
  }

  public allParametersValid(): boolean {
    return this.filters.every((f) => f.allParametersValid());
  }

  public anyParametersChanged(): boolean {
    return this.filters.some((f) => f.anyParameterChanged());
  }

  public numberInvalidParameters(): number {
    let sum = 0;
    this.filters.forEach((f) => {
      sum += f.numberInvalidParameters();
    });
    return sum;
  }

  public numberChangedParameters(): number {
    let sum = 0;
    this.filters.forEach((f) => {
      sum += f.numberChangedParameters();
    });
    return sum;
  }
}
