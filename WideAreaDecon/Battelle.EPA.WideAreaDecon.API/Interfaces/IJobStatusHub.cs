using System;
using System.Threading.Tasks;
using Battelle.EPA.WideAreaDecon.API.Enumeration.Job;

namespace Battelle.EPA.WideAreaDecon.API.Interfaces
{
    public interface IJobStatusHub
    {
        Task JobStatusChanged(Guid jobId, JobStatus newJobStatus);

        Task JobProgressChanged(Guid jobId, double newJobProgress);
    }
}
