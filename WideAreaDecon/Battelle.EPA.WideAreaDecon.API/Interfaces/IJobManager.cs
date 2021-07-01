using System;
using System.Collections.Generic;
using System.Linq;
using System.Threading.Tasks;
using Battelle.EPA.WideAreaDecon.API.Models.Job;
using Battelle.EPA.WideAreaDecon.API.Enumeration.Job;

namespace Battelle.EPA.WideAreaDecon.API.Interfaces
{
    /// <summary>
    /// Manages execution of jobs by the model
    /// </summary>
    public interface IJobManager
    {
        /// <summary>
        /// Adds a job to the job manager's execution queue
        /// </summary>
        /// <param name="job">The job to add to the queue</param>
        Task AddToQueue(JobRequest job);
        /// <summary>
        /// Gets the status of a requested job
        /// </summary>
        /// <param name="id">The job id</param>
        /// <returns>The status of the requested job</returns>
        JobStatus GetStatus(Guid id);
        /// <summary>
        /// Gets the requested job
        /// </summary>
        /// <param name="id">The job id</param>
        /// <returns>The requested job</returns>
        JobRequest GetJob(Guid id);
        //bool UpdateJob(JobRequest newJob);
    }
}
