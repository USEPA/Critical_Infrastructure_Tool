using Battelle.EPA.WideAreaDecon.API.Services;

namespace Battelle.EPA.WideAreaDecon.API.Application
{
    public class InputFileConfiguration
    {
        public ScenarioDefinitionService ScenarioParameters { get; set; }
        public BaselineParameterService BaselineParameters { get; set; }
    }
}