using Battelle.EPA.WideAreaDecon.InterfaceData.Enumeration.Providers;
using Battelle.EPA.WideAreaDecon.InterfaceData.Models.Parameter;

namespace Battelle.EPA.WideAreaDecon.InterfaceData.Interfaces.Providers
{
    public interface IParameterListProvider
    {
        ParameterListProviderType Type { get; }
        ParameterList GetParameterList();
    }
}