using Battelle.EPA.WideAreaDecon.InterfaceData.Enumeration.Providers;
using Battelle.EPA.WideAreaDecon.InterfaceData.Interfaces.Providers;
using Battelle.EPA.WideAreaDecon.InterfaceData.Models.Parameter;
using Newtonsoft.Json;
using Newtonsoft.Json.Converters;

namespace Battelle.EPA.WideAreaDecon.InterfaceData.Providers
{
    public class EmptyParameterListProvider : IParameterListProvider
    {
        [JsonConverter(typeof(StringEnumConverter))]
        public ParameterListProviderType Type => ParameterListProviderType.Empty;

        public ParameterList GetParameterList()
        {
            return new ParameterList(){Filters = new ParameterFilter[0]};
        }
    }
}