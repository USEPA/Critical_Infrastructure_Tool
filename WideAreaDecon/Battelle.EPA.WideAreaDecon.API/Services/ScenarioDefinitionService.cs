using Battelle.EPA.WideAreaDecon.InterfaceData.Interfaces.Providers;
using Battelle.EPA.WideAreaDecon.InterfaceData.Models.Parameter;
using Battelle.EPA.WideAreaDecon.InterfaceData.Utility.Json;
using Newtonsoft.Json;

namespace Battelle.EPA.WideAreaDecon.API.Services
{
    public class ScenarioDefinitionService
    {
        [JsonConverter(typeof(ParameterListProviderConverter))]
        public IParameterListProvider Provider { get; set; }


        public ParameterList GetParameterList()
        {
            return Provider.GetParameterList();
        }
    }
}