using System.Collections.Generic;
using Battelle.EPA.WideAreaDecon.InterfaceData.Enumeration.Parameter;
using Battelle.EPA.WideAreaDecon.InterfaceData;

namespace Battelle.EPA.WideAreaDecon.Model.Decontamination
{
    public interface ISuppliesCostCalculator
    {
        public double CalculateSuppliesCost(Dictionary<SurfaceType, ContaminationInformation> areaContaminated,
            Dictionary<SurfaceType, ApplicationMethod> treatmentMethods);
    }
}