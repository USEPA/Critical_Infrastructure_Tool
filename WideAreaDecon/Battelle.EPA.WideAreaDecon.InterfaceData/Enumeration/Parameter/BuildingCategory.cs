using Newtonsoft.Json;
using Newtonsoft.Json.Converters;

#pragma warning disable 1591
namespace Battelle.EPA.WideAreaDecon.InterfaceData.Enumeration.Parameter
{
    /// <summary>
    /// Categories of buildings utilized in the models
    ///
    /// Matches the categories defined by the FEMA HAZUS program
    /// </summary>
    [JsonConverter(typeof(StringEnumConverter))]
    public enum BuildingCategory
    {
        Residential,
        Commercial,
        Industrial,
        Agricultural,
        Religious,
        Government,
        Educational
    }
}