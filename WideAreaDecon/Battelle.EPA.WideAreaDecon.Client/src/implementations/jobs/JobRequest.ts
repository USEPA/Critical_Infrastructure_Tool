import JobStatus from '@/enums/jobs/jobStatus';
import IJobRequest from '@/interfaces/jobs/IJobRequest';
import { JsonProperty, Serializable } from 'typescript-json-serializer';
import ParameterWrapperList from '@/implementations/parameter/ParameterWrapperList';
import IJobResultRealization from '@/interfaces/jobs/results/IJobResultRealization';

@Serializable()
export default class JobRequest implements IJobRequest {
  @JsonProperty({
    // don't include in serialization
    onSerialize: () => undefined,
  })
  id: string;

  @JsonProperty()
  status: JobStatus;

  progress: number;

  @JsonProperty()
  defineScenario: ParameterWrapperList;

  @JsonProperty()
  modifyParameter: ParameterWrapperList;

  @JsonProperty()
  numberRealizations: number;

  @JsonProperty()
  seed1: number;

  @JsonProperty()
  seed2: number;

  @JsonProperty()
  results: IJobResultRealization[];

  constructor(
    status: JobStatus = JobStatus.new,
    defineScenario: ParameterWrapperList,
    modifyParameter: ParameterWrapperList,
    numberRealizations: number,
    seed1: number, // default seed values?
    seed2: number,
  ) {
    this.id = '';
    this.status = status;
    this.progress = 0;
    this.defineScenario = defineScenario;
    this.modifyParameter = modifyParameter;
    this.numberRealizations = numberRealizations;
    this.seed1 = seed1;
    this.seed2 = seed2;
    this.results = [];
  }
}
