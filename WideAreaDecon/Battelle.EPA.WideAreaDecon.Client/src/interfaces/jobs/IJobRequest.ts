import ParameterWrapperList from '@/implementations/parameter/ParameterWrapperList';
import JobStatus from '@/enums/jobs/jobStatus';
import IJobResultRealization from './results/IJobResultRealization';

export default interface IJobRequest {
  id: string;
  status: JobStatus;
  progress: number;
  defineScenario: ParameterWrapperList;
  modifyParameter: ParameterWrapperList;
  numberRealizations: number;
  seed1: number;
  seed2: number;
  results?: IJobResultRealization[];
}
