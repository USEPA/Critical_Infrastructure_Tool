using System;
using System.Collections.Generic;
using Battelle.EPA.WideAreaDecon.InterfaceData.Enumeration.Parameter;

namespace Battelle.EPA.WideAreaDecon.InterfaceData
{
    public class ScenarioRealization
    {
        public ScenarioRealization(Dictionary<BuildingCategory, Dictionary<SurfaceType, ContaminationInformation>> indoorBuildingsContaminated,
            Dictionary<SurfaceType, ContaminationInformation> outdoorAreasContaminated,
            Dictionary<SurfaceType, ContaminationInformation> undergroundBuildingsContaminated)
        {
            IndoorBuildingsContaminated = indoorBuildingsContaminated ??
                                          throw new ArgumentNullException(nameof(indoorBuildingsContaminated));
            OutdoorAreasContaminated= outdoorAreasContaminated ??
                                      throw new ArgumentNullException(nameof(outdoorAreasContaminated));
            UndergroundBuildingsContaminated= undergroundBuildingsContaminated ??
                                          throw new ArgumentNullException(nameof(undergroundBuildingsContaminated));
        }
        public Dictionary<BuildingCategory, Dictionary<SurfaceType, ContaminationInformation>> IndoorBuildingsContaminated { get; }
        public Dictionary<SurfaceType, ContaminationInformation> OutdoorAreasContaminated { get; }
        public Dictionary<SurfaceType, ContaminationInformation> UndergroundBuildingsContaminated { get; }
    }
}