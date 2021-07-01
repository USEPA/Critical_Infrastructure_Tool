using System.Collections.Generic;
using Battelle.EPA.WideAreaDecon.InterfaceData.Enumeration.Parameter;

namespace Battelle.EPA.WideAreaDecon.Model.Decontamination
{
    public interface IEfficacyCalculator
    {
        public Dictionary<SurfaceType, double> CalculateEfficacy(Dictionary<SurfaceType, double> _initialSporeLoading, Dictionary<SurfaceType, ApplicationMethod> treatmentMethods);
    }
}