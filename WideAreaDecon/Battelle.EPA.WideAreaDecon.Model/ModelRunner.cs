using System;
using System.Collections.Generic;
using System.Linq;
using Battelle.EPA.WideAreaDecon.InterfaceData;
using Battelle.EPA.WideAreaDecon.InterfaceData.Models.Parameter;
using Battelle.EPA.WideAreaDecon.InterfaceData.Models.Results;
using Battelle.EPA.WideAreaDecon.InterfaceData.Enumeration.Parameter;

namespace Battelle.EPA.WideAreaDecon.Model
{
    public class ModelRunner
    {
        private readonly ParameterList _scenarioParameters;
        private readonly DecontaminationPhase _phase;
        private readonly Dictionary<SurfaceType, ContaminationInformation> _buildingDetails;

        public ModelRunner(
            ParameterList scenarioParameters,
            DecontaminationPhase phase,
            Dictionary<SurfaceType, ContaminationInformation> buildingDetails)
        {
            _scenarioParameters = scenarioParameters;
            _phase = phase;
            _buildingDetails = buildingDetails;
        }

        public Results RunModel()
        {
            var parameterManager = new ParameterManager(
                _scenarioParameters.Filters.First(f => f.Name == "Characterization Sampling").Filters,
                _scenarioParameters.Filters.First(f => f.Name == "Source Reduction").Filters,
                _scenarioParameters.Filters.First(f => f.Name == "Decontamination").Filters,
                _scenarioParameters.Filters.First(f => f.Name == "Efficacy").Parameters,
                _scenarioParameters.Filters.First(f => f.Name == "Other").Filters,
                _scenarioParameters.Filters.First(f => f.Name == "Incident Command").Filters,
                _scenarioParameters.Filters.First(f => f.Name == "Cost per Parameter").Filters,
                _scenarioParameters.Filters.First(f => f.Name == "Decontamination Treatment Methods by Surface").Parameters);

            var calculatorManager = parameterManager.RedrawParameters(_buildingDetails, _phase);

            var resultsCalculator = parameterManager.SetDrawnParameters(calculatorManager);

            return resultsCalculator.CalculateResults(parameterManager, calculatorManager, _buildingDetails, _phase);
        }
    }
}
