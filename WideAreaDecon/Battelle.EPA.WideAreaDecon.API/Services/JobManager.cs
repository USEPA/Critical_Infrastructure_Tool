using System;
using System.Collections.Concurrent;
using System.Collections.Generic;
using System.Linq;
using System.Threading;
using System.Threading.Tasks;
using Battelle.EPA.WideAreaDecon.API.Enumeration.Job;
using Battelle.EPA.WideAreaDecon.API.Models.Job;
using Battelle.EPA.WideAreaDecon.API.Hubs;
using Battelle.EPA.WideAreaDecon.API.Interfaces;
using Battelle.EPA.WideAreaDecon.InterfaceData;
using Battelle.EPA.WideAreaDecon.InterfaceData.Enumeration.Parameter;
using Battelle.EPA.WideAreaDecon.InterfaceData.Models.Parameter.List;
using Battelle.EPA.WideAreaDecon.Model;
using Battelle.EPA.WideAreaDecon.InterfaceData.Models.Results;
using Microsoft.AspNetCore.SignalR;

namespace Battelle.EPA.WideAreaDecon.API.Services
{
    public class JobManager : IJobManager
    {
        private List<JobRequest> AllJobs { get; }
        private ConcurrentQueue<JobRequest> Queued { get; }
        private JobRequest Running { get; set; }
        private ConcurrentBag<JobRequest> Finished { get; }

        private CancellationTokenSource cancelCancellationTokenSource;

        private JobStatusUpdater _statusUpdater;
        private JobProgressUpdater _progressUpdater;

        public JobManager(IHubContext<JobStatusHub, IJobStatusHub> hub)
        {
            AllJobs = new List<JobRequest>();
            Queued = new ConcurrentQueue<JobRequest>();
            Running = null;
            Finished = new ConcurrentBag<JobRequest>();
            _statusUpdater = new JobStatusUpdater(hub);
            _progressUpdater = new JobProgressUpdater(hub);
            RunNextJob();
        }

        public async Task AddToQueue(JobRequest job)
        {
            AllJobs.Add(job);

            // allows for frontend to join hub group
            await Task.Delay(1000);

            await _statusUpdater.UpdateJobStatus(job, JobStatus.Queued);
            //_progressUpdater.UpdateJobProgress(job, 0.0);

            Queued.Enqueue(job);
        }

        private void RunNextJob()
        {
            if (Queued.IsEmpty)
            {
                Task.Run(() =>
                {
                    Task.Delay(500);
                    RunNextJob();
                });
                return;
            }

            cancelCancellationTokenSource = new CancellationTokenSource();

            if (Running != null)
            {
                throw new ApplicationException($"Trying to run new job while currently running job {Running.Id}");
            }
            if (!Queued.TryDequeue(out var newRun))
            {
                throw new ApplicationException($"Error trying to dequeue"); //TODO:: add more information to be helpful
            }

            Running = newRun;

            Task.Run(ConvertAndExecuteJob, cancelCancellationTokenSource.Token).ContinueWith(task => RunNextJob());

        }

        private Task ConvertAndExecuteJob() => Task.Run(async () =>
            {
                await _statusUpdater.UpdateJobStatus(Running, JobStatus.Running);

                try
                {
                    var extentOfContaminationParameters = Running.DefineScenario.Filters
                        .First(f => f.Name == "Extent of Contamination").Parameters;

                    var scenarioCreator = new ScenarioCreator(
                        extentOfContaminationParameters.First(p => p.MetaData.Name == "Area Contaminated") as EnumeratedParameter<DecontaminationPhase>,
                        extentOfContaminationParameters.First(p => p.MetaData.Name == "Loading") as EnumeratedParameter<DecontaminationPhase>,
                        extentOfContaminationParameters.First(p => p.MetaData.Name == "Indoor Contamination Breakout") as EnumeratedFraction<BuildingCategory>,
                        extentOfContaminationParameters.First(p => p.MetaData.Name == "Indoor Surface Type Breakout") as EnumeratedFraction<SurfaceType>,
                        extentOfContaminationParameters.First(p => p.MetaData.Name == "Outdoor Surface Type Breakout") as EnumeratedFraction<SurfaceType>,
                        extentOfContaminationParameters.First(p => p.MetaData.Name == "Underground Surface Type Breakout") as EnumeratedFraction<SurfaceType>);

                    var scenarios = new List<ScenarioRealization>();

                    for (int r = 0; r < Running.NumberRealizations; r++)
                    {
                        scenarios.Add(scenarioCreator.CreateRealizationScenario());
                    }

                    var parameterManager = new ParameterManager(
                        Running.ModifyParameter.Filters.First(f => f.Name == "Characterization Sampling").Filters,//
                        Running.ModifyParameter.Filters.First(f => f.Name == "Source Reduction").Filters,//
                        Running.ModifyParameter.Filters.First(f => f.Name == "Decontamination").Filters,//
                        Running.ModifyParameter.Filters.First(f => f.Name == "Efficacy").Parameters,//
                        Running.ModifyParameter.Filters.First(f => f.Name == "Other").Filters,
                        Running.ModifyParameter.Filters.First(f => f.Name == "Incident Command").Filters,//
                        Running.ModifyParameter.Filters.First(f => f.Name == "Cost per Parameter").Filters,//
                        Running.ModifyParameter.Filters.First(f => f.Name == "Decontamination Treatment Methods by Surface").Parameters);

                    var scenarioResults = new List<object>();

                    for (int s = 0; s < scenarios.Count(); s++)
                    {
                        var realizationResults = new Dictionary<DecontaminationPhase, object>();

                        //INDOOR SCENARIO
                        var buildingResults = new Dictionary<BuildingCategory, Results>();
                        foreach (var building in scenarios[s].IndoorBuildingsContaminated)
                        {
                            if (building.Value.Count > 0)
                            {
                                var indoorModelRunner = new ModelRunner(Running.ModifyParameter, DecontaminationPhase.Indoor, building.Value);

                                buildingResults.Add(building.Key, indoorModelRunner.RunModel());
                            }
                        }

                        realizationResults.Add(DecontaminationPhase.Indoor, buildingResults);

                        //OUTDOOR SCENARIO
                        var outdoorModelRunner = new ModelRunner(Running.ModifyParameter, DecontaminationPhase.Outdoor, scenarios[s].OutdoorAreasContaminated);

                        realizationResults.Add(DecontaminationPhase.Outdoor, outdoorModelRunner.RunModel());

                        //UNDERGROUND SCENARIO
                        var undergroundModelRunner = new ModelRunner(Running.ModifyParameter, DecontaminationPhase.Underground, scenarios[s].UndergroundBuildingsContaminated);

                        realizationResults.Add(DecontaminationPhase.Underground, undergroundModelRunner.RunModel());

                        //Store results for realization
                        scenarioResults.Add(realizationResults);
                    }

                    //Store results of model in job
                    Running.Results = scenarioResults;

                    await _statusUpdater.UpdateJobStatus(Running, JobStatus.Completed);
                    
                } catch (Exception e)
                {
                    Console.Error.WriteLine(e);
                    // TODO display error on front end?
                    await _statusUpdater.UpdateJobStatus(Running, JobStatus.Error);
                }

                Finished.Add(Running);
                Running = null;
            });

        public JobStatus GetStatus(Guid id) => GetJob(id)?.Status ?? JobStatus.Unknown;

        public JobRequest GetJob(Guid id) => AllJobs.FirstOrDefault(request => request.Id == id);

        //public bool UpdateJob(JobRequest newJob)
        //{
        //    var old = AllJobs.FirstOrDefault(request => request.Id == newJob.Id);
        //    if (old == null)
        //    {
        //        return false;
        //    }
        //    old = newJob;
        //    return true;
        //}
    }
}