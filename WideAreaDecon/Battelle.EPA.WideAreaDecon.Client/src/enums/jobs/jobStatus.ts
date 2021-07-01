// eslint-disable-next-line no-shadow
enum JobStatus {
  unknown = 'Unknown',
  error = 'Error',
  cancelled = 'Cancelled',
  new = 'New',
  queued = 'Queued',
  running = 'Running',
  completed = 'Completed',
}

export default JobStatus;
