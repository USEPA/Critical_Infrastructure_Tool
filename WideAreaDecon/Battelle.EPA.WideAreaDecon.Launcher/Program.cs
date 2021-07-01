using System;
using Newtonsoft.Json;
using System.IO;
using Battelle.EPA.WideAreaDecon.API.Services;
using Battelle.EPA.WideAreaDecon.API.Models.Job;
using Microsoft.AspNetCore.SignalR;
using Battelle.EPA.WideAreaDecon.API.Hubs;
using Battelle.EPA.WideAreaDecon.API.Interfaces;
using Battelle.EPA.WideAreaDecon.API.Enumeration.Job;

namespace Battelle.Epa.WideAreaDecon.Launcher
{// bin->Debug->netCoreapp3.1
    public class MakingJson
    {
        static void Main(string[] args1)
        {
               var path_to_newJobRequest = args1[0];
               
                string NewJobRequest = File.ReadAllText(path_to_newJobRequest);
                JobRequest Task2_JobRequest = JsonConvert.DeserializeObject<JobRequest>(NewJobRequest);
                Task2_JobRequest.Id = Guid.NewGuid();
                IHubContext<JobStatusHub, IJobStatusHub> __hub = null;
                var Task2_job = new JobManager(__hub);
                Task2_job.AddToQueue(Task2_JobRequest);
                var Task2status= Task2_job.GetStatus(Task2_JobRequest.Id);

                while (Task2status != JobStatus.Completed)
                {
                    Task2status = Task2_job.GetStatus(Task2_JobRequest.Id);
                }
                var task2job = Task2_job.GetJob(Task2_JobRequest.Id);
                var Task2Results = task2job.Results;
                var task2 = JsonConvert.SerializeObject(Task2Results);
                string fullPath = System.Reflection.Assembly.GetAssembly(typeof(MakingJson)).Location;

                //get the folder that's in
                string theDirectory = Path.GetDirectoryName(fullPath);
                Console.WriteLine(theDirectory);
                File.WriteAllText(theDirectory + "\\Task 2 Results.json", task2);
                
            }
        }
    }


  
        
                    
        




