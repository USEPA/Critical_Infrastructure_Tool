using System;
using System.Linq;
using Battelle.EPA.WideAreaDecon.API.Enumeration.Job;
using Battelle.EPA.WideAreaDecon.API.Models.Job;
using Battelle.EPA.WideAreaDecon.API.Hubs;
using Battelle.EPA.WideAreaDecon.API.Interfaces;
using Microsoft.AspNetCore.SignalR;

namespace Battelle.EPA.WideAreaDecon.API.Services
{
    /// <summary>
    /// Update's a job's progress and alerts hub clients of change
    /// </summary>
    public class JobProgressUpdater
    {
        private readonly IHubContext<JobStatusHub, IJobStatusHub> _hub;

        /// <summary>
        /// Default constructor
        /// </summary>
        /// <param name="hub">The hub context</param>
        public JobProgressUpdater(IHubContext<JobStatusHub, IJobStatusHub> hub)
        {
            _hub = hub;
        }

        /// <summary>
        /// Updates job progress
        /// </summary>
        /// <param name="job">The job to be updated</param>
        /// <param name="newJobProgress">The new job progress</param>
        public void UpdateJobProgress(JobRequest job, double newJobProgress)
        {
            job.Progress = newJobProgress;

            _hub.Clients.Group($"{job.Id}").JobProgressChanged(job.Id, job.Progress);
        }
    }
}
