using Newtonsoft.Json;
using Newtonsoft.Json.Converters;

namespace Battelle.EPA.WideAreaDecon.InterfaceData.Enumeration.Parameter
{
    [JsonConverter(typeof(StringEnumConverter))]
    public enum DecontaminationPhase
    {
        Indoor,
        Underground,
        Outdoor
    }
}