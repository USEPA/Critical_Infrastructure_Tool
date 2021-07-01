using System;
using Battelle.EPA.WideAreaDecon.API.Interfaces;
using Battelle.EPA.WideAreaDecon.API.Services;
using System.Threading.Tasks;
using Microsoft.AspNetCore.SignalR;
using Battelle.EPA.WideAreaDecon.API.Enumeration.Job;

namespace Battelle.EPA.WideAreaDecon.API.Hubs
{
    /// <summary>
    /// Hub which enables websocket connections to update job status and progress
    /// </summary>
    public class JobStatusHub : Hub<IJobStatusHub>
    {
        private readonly IJobManager _jobManager;
        private readonly JobStatusUpdater _statusUpdater;

        public JobStatusHub(IJobManager jobManager, JobStatusUpdater statusUpdater)
        {
            _jobManager = jobManager;
            _statusUpdater = statusUpdater;
        }

        /// <summary>
        /// Allows user to request to join group receiving status updates on a given job
        /// </summary>
        /// <param name="jobId">The job id</param>
        /// <returns></returns>
        public async Task JoinWatchJobGroup(Guid jobId)
        {
            try
            {
                var job = _jobManager.GetJob(jobId);

                if (job == null)
                {
                    return;
                }

                await Groups.AddToGroupAsync(Context.ConnectionId, $"{jobId}");
                //await Clients.Group($"{jobId}").JobStatusChanged(jobId, job.Status);
            }
            catch (Exception e)
            {
                Console.WriteLine(e);
            }
        }

        /// <summary>
        /// User request to leave the group
        /// </summary>
        /// <param name="jobId">The job</param>
        /// <returns></returns>
        public async Task LeaveWatchJobGroup(Guid jobId)
        {
            try
            {
                await Groups.RemoveFromGroupAsync(Context.ConnectionId, $"{jobId}");
            }
            catch (Exception e)
            {
                Console.WriteLine(e);
            }
        }

        /// <summary>
        /// Updates the progress of a job to a new value
        /// </summary>
        /// <param name="jobId">The job being updated</param>
        /// <param name="newProgress">The new progress value</param>
        public void UpdateJobProgress(Guid jobId, double newProgress)
        {
            try
            {
                var oldJob = _jobManager.GetJob(jobId);
                oldJob.Progress = newProgress;
                // TODO add update progress method to job manager
            }
            catch (Exception e)
            {
                Console.WriteLine(e);
            }
        }

        /// <summary>
        /// Updates the status of a job to a new value
        /// </summary>
        /// <param name="jobId">The job being updated</param>
        /// <param name="newJobStatus">The new job status</param>
        public void UpdateJobStatus(Guid jobId, JobStatus newJobStatus)
        {
            try
            {
                var oldJob = _jobManager.GetJob(jobId);
                var oldJobStatus = oldJob.Status;
                if (oldJobStatus == newJobStatus)
                {
                    return;
                }
                _statusUpdater.UpdateJobStatus(oldJob, newJobStatus);

                //_jobManager.UpdateJob(oldJob);
                Clients.Group($"{jobId}").JobStatusChanged(jobId, newJobStatus);
            }
            catch (Exception e)
            {
                Console.WriteLine(e);
            }
        }
    }
}
