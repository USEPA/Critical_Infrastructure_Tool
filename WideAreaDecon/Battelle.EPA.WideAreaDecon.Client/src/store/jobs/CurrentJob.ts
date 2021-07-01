import ICurrentJob from '@/interfaces/store/jobs/ICurrentJob';
import JobRequest from '@/implementations/jobs/JobRequest';
import JobStatus from '@/enums/jobs/jobStatus';
import ParameterWrapperList from '@/implementations/parameter/ParameterWrapperList';

export default class CurrentJob implements ICurrentJob {
  currentJob = new JobRequest(JobStatus.unknown, new ParameterWrapperList(), new ParameterWrapperList(), 0, 0, 0);
}
