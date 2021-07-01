import JobStatus from '@/enums/jobs/jobStatus';
import { HttpTransportType, HubConnection, HubConnectionBuilder, LogLevel } from '@aspnet/signalr';

export default class JobManager {
  readonly apiEndpoint = '/api/job-status-hub';

  readonly jobStatusChangedEventName = 'JobStatusChanged';

  readonly jobProgressChangedEventName = 'JobProgressChanged';

  jobId: string;

  connection: HubConnection;

  constructor(
    jobId: string,
    updateJobStatusCallback: (newStatus: JobStatus) => void,
    updateJobProgressCallback: (newProgress: number) => void,
  ) {
    this.jobId = jobId;
    this.connection = new HubConnectionBuilder()
      .withUrl(this.apiEndpoint, {
        transport: HttpTransportType.WebSockets,
      })
      .configureLogging(LogLevel.Debug)
      .build();

    // eslint-disable-next-line @typescript-eslint/no-this-alias
    const self = this;
    this.connection.on(self.jobStatusChangedEventName, (id: string, newStatus: JobStatus) => {
      if (self.jobId !== id) {
        return;
      }
      updateJobStatusCallback(newStatus);
    });

    this.connection.on(self.jobProgressChangedEventName, (id: string, newProgress: number) => {
      if (self.jobId !== id) {
        return;
      }
      updateJobProgressCallback(newProgress);
    });
  }

  async StartWatchJobProgress(): Promise<void> {
    await this.connection.start();
    await this.connection.send('JoinWatchJobGroup', this.jobId);
  }

  async StopWatchJobProgress(): Promise<void> {
    await this.connection.send('LeaveWatchJobGroup', this.jobId);
    await this.connection.stop();
  }
}
