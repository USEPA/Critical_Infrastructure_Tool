import { MutationTree } from 'vuex';
import IRootState from '@/interfaces/store/IRootState';
import JobRequest from '@/implementations/jobs/JobRequest';
import JobStatus from '@/enums/jobs/jobStatus';

const currentJobMutations: MutationTree<IRootState> = {
  setCurrentJob(state: IRootState, newJob: JobRequest) {
    state.currentJob = newJob;
  },

  updateJobId(state: IRootState, id: string) {
    state.currentJob.id = id;
  },

  updateJobStatus(state: IRootState, status: JobStatus) {
    state.currentJob.status = status;
  },

  updateJobProgress(state: IRootState, progress: number) {
    state.currentJob.progress = progress;
  },
};

export default currentJobMutations;
