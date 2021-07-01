import { JsonProperty, Serializable } from 'typescript-json-serializer';
import ParameterFilter from './ParameterFilter';
import ParameterWrapperList from './ParameterWrapperList';

@Serializable()
export default class ParameterList {
  @JsonProperty()
  version: number;

  @JsonProperty({
    predicate: () => {
      return ParameterFilter;
    },
  })
  filters: Array<ParameterFilter>;

  constructor(version = 0, filters?: ParameterFilter[]) {
    this.version = version;
    this.filters = filters !== undefined ? filters : new Array<ParameterFilter>();
  }

  public toWrapperList(): ParameterWrapperList {
    return new ParameterWrapperList(
      this.version,
      this.filters.map((f) => f.toParameterWrapperFilter(null)),
    );
  }

  public allParametersValid(): boolean {
    return this.filters.every((f) => f.allParametersValid());
  }

  public numberInvalidParameters(): number {
    let sum = 0;
    this.filters.forEach((f) => {
      sum += f.numberInvalidParameters();
    });
    return sum;
  }
}
