using System.Collections.Generic;
using Battelle.EPA.WideAreaDecon.InterfaceData;
using Battelle.EPA.WideAreaDecon.InterfaceData.Enumeration.Parameter;

namespace Battelle.EPA.WideAreaDecon.Model.CharacterizationSampling
{
    public interface ILaborCostCalculator
    {
        public double CalculateLaborCost(double workDays, double _numberTeams, double personnelRoundTripDays, double _fractionSampledWipe, double _fractionSampledHepa, Dictionary<SurfaceType, ContaminationInformation> _areaContaminated);

        public double CalculateLaborDays(double workDays);
    }
}