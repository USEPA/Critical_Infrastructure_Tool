using System;
using System.Runtime.Serialization;
using Newtonsoft.Json;
using Newtonsoft.Json.Converters;

namespace Battelle.EPA.WideAreaDecon.InterfaceData.Enumeration.Parameter
{
    [JsonConverter(typeof(StringEnumConverter))]
    public enum SurfaceType
    {
        [EnumMember(Value = "Indoor Walls")]
        IndoorWalls,

        [EnumMember(Value = "Indoor Ceilings")]
        IndoorCeilings,

        [EnumMember(Value = "Indoor Carpet")] 
        IndoorCarpet,

        [EnumMember(Value = "Indoor Non-Carpet")]
        IndoorNonCarpet,

        [EnumMember(Value = "Indoor HVAC")] 
        IndoorHvac,

        [EnumMember(Value = "Indoor Miscellaneous")]
        IndoorMisc,

        [EnumMember(Value = "Outdoor Exterior")]
        OutdoorExterior,

        [EnumMember(Value = "Pavement")] 
        Pavement,

        [EnumMember(Value = "Roofing")] 
        Roofing,

        [EnumMember(Value = "Water")] 
        Water,

        [EnumMember(Value = "Soil")] 
        Soil,

        [EnumMember(Value = "Outdoor Miscellaneous")]
        OutdoorMisc,

        [EnumMember(Value = "Underground Walls")]
        UndergroundWalls,

        [EnumMember(Value = "Underground Ceilings")]
        UndergroundCeilings,

        [EnumMember(Value = "Underground Carpet")]
        UndergroundCarpet,

        [EnumMember(Value = "Underground Non-Carpet")]
        UndergroundNonCarpet,

        [EnumMember(Value = "Underground HVAC")]
        UndergroundHvac,

        [EnumMember(Value = "Underground Miscellaneous")]
        UndergroundMisc
    }
    public static class SurfaceTypeHelper
    {
        public static readonly SurfaceType[] IndoorSurfaceTypes = {
            SurfaceType.IndoorWalls,
            SurfaceType.IndoorCeilings,
            SurfaceType.IndoorCarpet,
            SurfaceType.IndoorNonCarpet,
            SurfaceType.IndoorHvac,
            SurfaceType.IndoorMisc,
        };


        public static readonly SurfaceType[] OutdoorSurfaceTypes = {
            SurfaceType.OutdoorExterior,
            SurfaceType.Pavement,
            SurfaceType.Roofing,
            SurfaceType.Water,
            SurfaceType.Soil,
            SurfaceType.OutdoorMisc,
        };


        public static readonly SurfaceType[] UndergroundSurfaceTypes = {
            SurfaceType.UndergroundWalls,
            SurfaceType.UndergroundCeilings,
            SurfaceType.UndergroundCarpet,
            SurfaceType.UndergroundNonCarpet,
            SurfaceType.UndergroundMisc,
            SurfaceType.UndergroundHvac,
        };

        public static SurfaceType[] GetSurfaceTypesForPhase(DecontaminationPhase phase)
        {
            return phase switch
            {
                DecontaminationPhase.Indoor => IndoorSurfaceTypes,
                DecontaminationPhase.Outdoor => OutdoorSurfaceTypes,
                DecontaminationPhase.Underground => UndergroundSurfaceTypes,
                _ => throw new ArgumentOutOfRangeException()
            };
        }
    }
}