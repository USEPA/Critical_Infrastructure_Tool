import IJobProvider from '@/interfaces/providers/IJobProvider';

export default interface ICreateJobRequestPayload {
  jobProvider: IJobProvider;
  numberRealizations: number;
  seed1: number;
  seed2: number;
}
