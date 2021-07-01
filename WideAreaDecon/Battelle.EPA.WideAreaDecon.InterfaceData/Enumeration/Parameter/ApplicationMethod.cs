using System.Runtime.Serialization;
using Newtonsoft.Json;
using Newtonsoft.Json.Converters;
using System;
using System.Collections.Generic;
using System.Linq;

namespace Battelle.EPA.WideAreaDecon.InterfaceData.Enumeration.Parameter
{
    [JsonConverter(typeof(StringEnumConverter))]
    public enum ApplicationMethod
    {
        [EnumMember(Value = "Aerosol")] 
        Aerosol,

        [EnumMember(Value = "Foam Spray")] 
        FoamSpray,

        [EnumMember(Value = "Fogging")] 
        Fogging,

        [EnumMember(Value = "Fumigation")] 
        Fumigation,

        [EnumMember(Value = "Gel")] 
        Gel,

        [EnumMember(Value = "Liquid Immersion")]
        LiquidImmersion,

        [EnumMember(Value = "Liquid Spray")] 
        LiquidSpray,

        [EnumMember(Value = "Liquid Suspension")]
        LiquidSuspension,

        [EnumMember(Value = "Liquid Wipe")] 
        LiquidWipe,

        [EnumMember(Value = "Physical")] 
        Physical
    }

    public static class ApplicableApplicationMethodHelper
    {
        public static readonly List<ApplicationMethod> IndoorWallsMethods = new List<ApplicationMethod> {
            ApplicationMethod.Aerosol,
            ApplicationMethod.FoamSpray,
            ApplicationMethod.Fogging,
            ApplicationMethod.Fumigation,
            ApplicationMethod.Gel,
            ApplicationMethod.LiquidImmersion,
            ApplicationMethod.LiquidSpray,
            ApplicationMethod.LiquidWipe,
            ApplicationMethod.Physical
        };

        public static readonly List<ApplicationMethod> IndoorCeilingsMethods = new List<ApplicationMethod> { 
            ApplicationMethod.FoamSpray,
            ApplicationMethod.Fogging,
            ApplicationMethod.Fumigation,
            ApplicationMethod.Gel,
            ApplicationMethod.LiquidImmersion,
            ApplicationMethod.LiquidSpray,
            ApplicationMethod.LiquidWipe,
            ApplicationMethod.Physical
        };

        public static readonly List<ApplicationMethod> IndoorCarpetMethods = new List<ApplicationMethod> {
            ApplicationMethod.FoamSpray,
            ApplicationMethod.Fogging,
            ApplicationMethod.Fumigation,
            ApplicationMethod.LiquidImmersion,
            ApplicationMethod.LiquidSpray,
            ApplicationMethod.Physical
        };

        public static readonly List<ApplicationMethod> IndoorNonCarpetMethods = new List<ApplicationMethod> {
            ApplicationMethod.Aerosol,
            ApplicationMethod.FoamSpray,
            ApplicationMethod.Fogging,
            ApplicationMethod.Fumigation,
            ApplicationMethod.Gel,
            ApplicationMethod.LiquidImmersion,
            ApplicationMethod.LiquidSpray,
            ApplicationMethod.LiquidWipe,
            ApplicationMethod.Physical
        };

        public static readonly List<ApplicationMethod> IndoorHvacMethods = new List<ApplicationMethod> {
            ApplicationMethod.FoamSpray,
            ApplicationMethod.Fogging,
            ApplicationMethod.Fumigation,
            ApplicationMethod.Gel,
            ApplicationMethod.LiquidSpray,
            ApplicationMethod.LiquidWipe,
            ApplicationMethod.Physical
        };

        public static readonly List<ApplicationMethod> IndoorMiscMethods = new List<ApplicationMethod> {
            ApplicationMethod.Aerosol,
            ApplicationMethod.FoamSpray,
            ApplicationMethod.Fumigation,
            ApplicationMethod.LiquidImmersion,
            ApplicationMethod.LiquidSpray,
            ApplicationMethod.LiquidWipe,
            ApplicationMethod.Physical
        };

        public static readonly List<ApplicationMethod> OutdoorExteriorMethods = new List<ApplicationMethod> {
            ApplicationMethod.Aerosol,
            ApplicationMethod.FoamSpray,
            ApplicationMethod.Fumigation,
            ApplicationMethod.LiquidSpray,
            ApplicationMethod.LiquidWipe,
            ApplicationMethod.Physical
        };

        public static readonly List<ApplicationMethod> PavementMethods = new List<ApplicationMethod> { 
            ApplicationMethod.FoamSpray,
            ApplicationMethod.LiquidImmersion,
            ApplicationMethod.LiquidSpray,
            ApplicationMethod.Physical
        };

        public static readonly List<ApplicationMethod> RoofingMethods = new List<ApplicationMethod> {
            ApplicationMethod.Aerosol,
            ApplicationMethod.FoamSpray,
            ApplicationMethod.Fogging,
            ApplicationMethod.Fumigation,
            ApplicationMethod.LiquidSpray,
            ApplicationMethod.Physical
        };

        public static readonly List<ApplicationMethod> WaterMethods = new List<ApplicationMethod> { 
            ApplicationMethod.LiquidSuspension,
            ApplicationMethod.Physical
        };

        public static readonly List<ApplicationMethod> SoilMethods = new List<ApplicationMethod> {
            ApplicationMethod.FoamSpray,
            ApplicationMethod.Fumigation,
            ApplicationMethod.LiquidSpray,
            ApplicationMethod.Physical
        };

        public static readonly List<ApplicationMethod> OutdoorMiscMethods = new List<ApplicationMethod> {
            ApplicationMethod.Aerosol,
            ApplicationMethod.FoamSpray,
            ApplicationMethod.Fogging,
            ApplicationMethod.Fumigation,
            ApplicationMethod.Gel,
            ApplicationMethod.LiquidImmersion,
            ApplicationMethod.LiquidSpray,
            ApplicationMethod.LiquidWipe,
            ApplicationMethod.Physical
        };

        public static readonly List<ApplicationMethod> UndergroundWallsMethods = new List<ApplicationMethod> {
            ApplicationMethod.Aerosol,
            ApplicationMethod.FoamSpray,
            ApplicationMethod.Fogging,
            ApplicationMethod.Fumigation,
            ApplicationMethod.Gel,
            ApplicationMethod.LiquidImmersion,
            ApplicationMethod.LiquidSpray,
            ApplicationMethod.LiquidWipe,
            ApplicationMethod.Physical
        };

        public static readonly List<ApplicationMethod> UndergroundCeilingsMethods = new List<ApplicationMethod> {
            ApplicationMethod.FoamSpray,
            ApplicationMethod.Fogging,
            ApplicationMethod.Fumigation,
            ApplicationMethod.Gel,
            ApplicationMethod.LiquidImmersion,
            ApplicationMethod.LiquidSpray,
            ApplicationMethod.LiquidWipe,
            ApplicationMethod.Physical
        };

        public static readonly List<ApplicationMethod> UndergroundCarpetMethods = new List<ApplicationMethod> {
            ApplicationMethod.FoamSpray,
            ApplicationMethod.Fogging,
            ApplicationMethod.Fumigation,
            ApplicationMethod.LiquidImmersion,
            ApplicationMethod.LiquidSpray,
            ApplicationMethod.Physical
        };

        public static readonly List<ApplicationMethod> UndergroundNonCarpetMethods = new List<ApplicationMethod> {
            ApplicationMethod.Aerosol,
            ApplicationMethod.FoamSpray,
            ApplicationMethod.Fogging,
            ApplicationMethod.Fumigation,
            ApplicationMethod.Gel,
            ApplicationMethod.LiquidImmersion,
            ApplicationMethod.LiquidSpray,
            ApplicationMethod.LiquidWipe,
            ApplicationMethod.Physical
        };

        public static readonly List<ApplicationMethod> UndergroundHvacMethods = new List<ApplicationMethod> {
            ApplicationMethod.FoamSpray,
            ApplicationMethod.Fogging,
            ApplicationMethod.Fumigation,
            ApplicationMethod.Gel,
            ApplicationMethod.LiquidSpray,
            ApplicationMethod.LiquidWipe,
            ApplicationMethod.Physical
        };

        public static readonly List<ApplicationMethod> UndergroundMiscMethods = new List<ApplicationMethod> {
            ApplicationMethod.Aerosol,
            ApplicationMethod.FoamSpray,
            ApplicationMethod.Fogging,
            ApplicationMethod.Fumigation,
            ApplicationMethod.Gel,
            ApplicationMethod.LiquidImmersion,
            ApplicationMethod.LiquidSpray,
            ApplicationMethod.LiquidWipe,
            ApplicationMethod.Physical
        };

        public static List<ApplicationMethod> GetApplicationMethodsForSurface(SurfaceType surface)
        {
            return surface switch
            {
                SurfaceType.IndoorWalls => IndoorWallsMethods,
                SurfaceType.IndoorCeilings => IndoorCeilingsMethods,
                SurfaceType.IndoorCarpet => IndoorCarpetMethods,
                SurfaceType.IndoorNonCarpet => IndoorNonCarpetMethods,
                SurfaceType.IndoorHvac => IndoorHvacMethods,
                SurfaceType.IndoorMisc => IndoorMiscMethods,
                SurfaceType.OutdoorExterior => OutdoorExteriorMethods,
                SurfaceType.Pavement => PavementMethods,
                SurfaceType.Roofing => RoofingMethods,
                SurfaceType.Water => WaterMethods,
                SurfaceType.Soil => SoilMethods,
                SurfaceType.OutdoorMisc => OutdoorMiscMethods,
                SurfaceType.UndergroundWalls => UndergroundWallsMethods,
                SurfaceType.UndergroundCeilings => UndergroundCeilingsMethods,
                SurfaceType.UndergroundCarpet => UndergroundCarpetMethods,
                SurfaceType.UndergroundNonCarpet => UndergroundNonCarpetMethods,
                SurfaceType.UndergroundHvac => UndergroundHvacMethods,
                SurfaceType.UndergroundMisc => UndergroundNonCarpetMethods,
                _ => throw new ArgumentOutOfRangeException()
            };
        }
    }
}