using System.Runtime.Serialization;
using Newtonsoft.Json;
using Newtonsoft.Json.Converters;

namespace Battelle.EPA.WideAreaDecon.InterfaceData.Enumeration.Parameter
{
    [JsonConverter(typeof(StringEnumConverter))]
    public enum PhaseCategory
    {
        [EnumMember(Value = "Incident Command")] IncidentCommand,

        [EnumMember(Value = "Characterization Sampling")] CharacterizationSampling,

        [EnumMember(Value = "Source Reduction")] SourceReduction,

        [EnumMember(Value = "Decontamination")] Decontamination,

        [EnumMember(Value = "Other")] Other
    }
}
