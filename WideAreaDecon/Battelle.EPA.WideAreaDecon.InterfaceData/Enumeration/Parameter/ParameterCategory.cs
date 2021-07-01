using System.Runtime.Serialization;
using Newtonsoft.Json;
using Newtonsoft.Json.Converters;

namespace Battelle.EPA.WideAreaDecon.InterfaceData.Enumeration.Parameter
{
    [JsonConverter(typeof(StringEnumConverter))]
    public enum ParameterCategory
    {
        [EnumMember(Value = "Personnel")] Personnel,

        [EnumMember(Value = "Safety")] Safety,

        [EnumMember(Value = "Supplies")] Supplies,

        [EnumMember(Value = "Logistic")] Logistic,

        [EnumMember(Value = "Eff")] Eff
    }
}
