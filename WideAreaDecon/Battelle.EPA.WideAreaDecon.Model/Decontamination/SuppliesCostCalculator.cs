using System.Collections.Generic;
using System.Linq;
using System;
using Battelle.EPA.WideAreaDecon.InterfaceData.Enumeration.Parameter;
using Battelle.EPA.WideAreaDecon.InterfaceData;

namespace Battelle.EPA.WideAreaDecon.Model.Decontamination
{
    public class SuppliesCostCalculator : ISuppliesCostCalculator
    {
        private readonly double _deconAgentCostPerVolume;
        private readonly double _deconAgentVolume;
        private readonly Dictionary<SurfaceType, double> _deconAgentVolumeBySurface;
        private readonly double _deconMaterialsCost;

        public SuppliesCostCalculator(
            double deconAgentCostPerVolume,
            double deconMaterialsCost,
            double deconAgentVolume,
            Dictionary<SurfaceType, double> deconAgentVolumeBySurface)
        {
            _deconAgentCostPerVolume = deconAgentCostPerVolume;
            _deconMaterialsCost = deconMaterialsCost;
            _deconAgentVolume = deconAgentVolume;
            _deconAgentVolumeBySurface = deconAgentVolumeBySurface;
        }

        public double CalculateSuppliesCost(Dictionary<SurfaceType, ContaminationInformation> areaContaminated,
            Dictionary<SurfaceType, ApplicationMethod> treatmentMethods)
        {
            var totalContaminationArea = areaContaminated.Sum(x => x.Value.AreaContaminated);

            return (_deconMaterialsCost * totalContaminationArea) + NonFoggingSuppliesCostCalculator(areaContaminated, treatmentMethods) + FoggingSuppliesCostCalculator(areaContaminated, treatmentMethods);
        }

        private double NonFoggingSuppliesCostCalculator(
            Dictionary<SurfaceType, ContaminationInformation> areaContaminated,
            Dictionary<SurfaceType, ApplicationMethod> treatmentMethods)
        {
            var surfaceContamination = new Dictionary<SurfaceType, double>();
            foreach (SurfaceType surface in areaContaminated.Keys.ToList())
            {
                if (treatmentMethods[surface] != ApplicationMethod.Fogging && treatmentMethods[surface] != ApplicationMethod.Fumigation)
                {
                    surfaceContamination.Add(surface, areaContaminated[surface].AreaContaminated);
                }
                else
                {
                    surfaceContamination.Add(surface, 0.0);
                }
            }

            var nonFoggingContaminationArea = surfaceContamination.Values.Sum();
            var agentNeededPerTreatment = _deconAgentVolumeBySurface.Values.Zip(surfaceContamination.Values, (x, y) => x * y).Sum();
            return agentNeededPerTreatment * _deconAgentCostPerVolume;
        }

        private double FoggingSuppliesCostCalculator(
            Dictionary<SurfaceType, ContaminationInformation> areaContaminated,
            Dictionary<SurfaceType, ApplicationMethod> treatmentMethods)
        {
            var foggingSuppliesCost = 0.0;

            if (treatmentMethods.ContainsValue(ApplicationMethod.Fogging) || treatmentMethods.ContainsValue(ApplicationMethod.Fumigation))
            {
                var totalContaminationArea = areaContaminated.Sum(x => x.Value.AreaContaminated);

                foggingSuppliesCost = totalContaminationArea * GlobalConstants.RoomHeight * _deconAgentVolume * _deconAgentCostPerVolume;
            }

            return foggingSuppliesCost;
        }
    }
}