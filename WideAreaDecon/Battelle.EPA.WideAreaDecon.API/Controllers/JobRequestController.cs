using System;
using Battelle.EPA.WideAreaDecon.API.Enumeration.Job;
using Battelle.EPA.WideAreaDecon.API.Models.Job;
using Battelle.EPA.WideAreaDecon.API.Interfaces;
using Microsoft.AspNetCore.Mvc;

namespace Battelle.EPA.WideAreaDecon.API.Controllers
{
    [Route("api/[controller]")]
    [ApiController]
    public class JobRequestController : ControllerBase
    {

        private readonly IJobManager _jobManager;

        /// <summary>
        /// Default constructor, requires a non-null provider
        /// </summary>
        /// <param name="jobManager"></param>
        public JobRequestController(IJobManager jobManager)
        {
            _jobManager = jobManager;
        }

        /// <summary>
        /// Adds new job to the job manager queue
        /// </summary>
        /// <returns>The new job's id</returns>
        [HttpPost]
        [ProducesResponseType(typeof(Guid), 200)]
        public Guid AddNewJob([FromBody] JobRequest job)
        {
            if (job == null)
            {
                throw new ApplicationException("Need to return bad request to fronted");
                // return bad response
            }

            job.Id = Guid.NewGuid();

            _jobManager.AddToQueue(job);

            return job.Id;
        }

        [HttpGet("status")]
        [ProducesResponseType(typeof(JobStatus), 200)]
        public JobStatus GetJobStatus(Guid id)
        {
            return _jobManager.GetStatus(id);
        }

        [HttpGet]
        [ProducesResponseType(typeof(JobRequest), 200)]
        public JobRequest GetJob(Guid id)
        {
            return _jobManager.GetJob(id);
        }
    }
}