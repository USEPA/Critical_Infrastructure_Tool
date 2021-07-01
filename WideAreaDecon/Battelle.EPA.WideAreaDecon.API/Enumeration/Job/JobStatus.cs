using System.Runtime.Serialization;
using Newtonsoft.Json;
using Newtonsoft.Json.Converters;

namespace Battelle.EPA.WideAreaDecon.API.Enumeration.Job
{
    [JsonConverter(typeof(StringEnumConverter))]
    public enum JobStatus
    {
        [EnumMember(Value = "Unknown")]
        Unknown = -3,
        [EnumMember(Value = "Error")]
        Error = -2,
        [EnumMember(Value = "Cancelled")]
        Cancelled,
        [EnumMember(Value = "New")]
        New,
        [EnumMember(Value = "Queued")]
        Queued,
        [EnumMember(Value = "Running")]
        Running,
        [EnumMember(Value = "Completed")]
        Completed,
    }
}