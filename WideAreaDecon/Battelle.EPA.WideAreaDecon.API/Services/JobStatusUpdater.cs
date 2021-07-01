using System;
using System.Linq;
using Battelle.EPA.WideAreaDecon.API.Enumeration.Job;
using Battelle.EPA.WideAreaDecon.API.Models.Job;
using Battelle.EPA.WideAreaDecon.API.Hubs;
using Battelle.EPA.WideAreaDecon.API.Interfaces;
using Microsoft.AspNetCore.SignalR;
using System.Threading.Tasks;

namespace Battelle.EPA.WideAreaDecon.API.Services
{
    /// <summary>
    /// Updates a job's status and alerts hub clients of change
    /// </summary>
    public class JobStatusUpdater
    {
        private readonly JobStatus[] _initialJobStatuses = new[] { JobStatus.New, JobStatus.Queued };

        private readonly JobStatus[] _runningJobStatuses = new[] { JobStatus.Running };

        private readonly JobStatus[] _completedJobStatuses = new[] { JobStatus.Completed };

        private readonly IHubContext<JobStatusHub, IJobStatusHub> _hub;

        /// <summary>
        /// Default constructor
        /// </summary>
        /// <param name="hub">The hub context</param>
        public JobStatusUpdater(IHubContext<JobStatusHub, IJobStatusHub> hub)
        {
            _hub = hub;
        }

        /// <summary>
        /// Updates job status
        /// </summary>
        /// <param name="job">The job to be updated</param>
        /// <param name="newJobStatus">The new job status</param>
        public async Task UpdateJobStatus(JobRequest job, JobStatus newJobStatus)
        {
            var oldJobStatus = job.Status;
            job.Status = newJobStatus;
            CheckIfJobStarted(job, oldJobStatus);
            CheckIfJobCompleted(job, oldJobStatus);
            if (_hub != null)
            {
                await _hub.Clients.Group($"{job.Id}").JobStatusChanged(job.Id, job.Status);
            }
            
           
        }

        private void CheckIfJobStarted(JobRequest job, JobStatus oldStatus)
        {
            if (!_initialJobStatuses.Contains(oldStatus))
            {
                return;
            }

            //// TODO Track time it takes to complete a job
            //if (_runningJobStatuses.Contains(job.Status))
            //{
            //    job.Started = DateTime.Now;
            //}
        }

        private void CheckIfJobCompleted(JobRequest job, JobStatus oldJobStatus)
        {
            if (!_runningJobStatuses.Contains(oldJobStatus))
            {
                return;
            }

            //// TODO Track time it takes to complete a job
            //if (_completedJobStatuses.Contains(job.Status))
            //{
            //    job.Completed = DateTime.Now;
            //}
        }
    }
}
