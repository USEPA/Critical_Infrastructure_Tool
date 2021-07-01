using Battelle.EPA.WideAreaDecon.Model.CharacterizationSampling;
using System.Collections.Generic;
using Battelle.EPA.WideAreaDecon.InterfaceData.Enumeration.Parameter;
using Battelle.EPA.WideAreaDecon.Model.Services;
using Battelle.EPA.WideAreaDecon.InterfaceData;

namespace Battelle.EPA.WideAreaDecon.Model.CharacterizationSampling
{
    public class CharacterizationSamplingCostCalculator : ICharacterizationSamplingCalculatorFactory
    {
        public LaborCostCalculator Calculator_labor { get; set; }
        public SuppliesCostCalculator Calculator_supplies { get; set; }
        public EntrancesExitsCostCalculator Calculator_entEx { get; set; }
        public AnalysisQuantityCostCalculator Calculator_analysis { get; set; }
        public PhaseLagCalculator Calculator_phaseLag { get; set; }

        public double CalculateTime(double _numberTeams, double _fractionSampledWipe, double _fractionSampledHepa, Dictionary<SurfaceType, ContaminationInformation> _areaContaminated)
        {
            return Calculator_supplies.CalculateWorkDays(_numberTeams, _fractionSampledWipe, _fractionSampledHepa, _areaContaminated);
        }

        public double CalculatePhaseLag(int _numberLabs, double _sampleTimeTransmitted, double _fractionSampledWipe, double _fractionSampledHepa, Dictionary<SurfaceType, ContaminationInformation> _areaContaminated)
        {
            return Calculator_phaseLag.CalculatePhaseLagTime(_numberLabs, _sampleTimeTransmitted, _fractionSampledWipe, _fractionSampledHepa, _areaContaminated);
        }

        public double CalculateCost(double workDays, double _numberTeams, double _fractionSampledWipe, double _fractionSampledHepa, Dictionary<SurfaceType, ContaminationInformation> _areaContaminated, double personnelRoundTripDays,
             Dictionary<PpeLevel, double> ppePerLevelPerTeam)
        {
            var suppliesCosts = Calculator_supplies.CalculateSuppliesCost(_numberTeams, _fractionSampledWipe, _fractionSampledHepa, _areaContaminated);
            var laborCosts = Calculator_labor.CalculateLaborCost(workDays, _numberTeams, personnelRoundTripDays, _fractionSampledWipe, _fractionSampledHepa, _areaContaminated);
            var entExCosts = Calculator_entEx.CalculateEntrancesExitsCost(workDays, _numberTeams, ppePerLevelPerTeam, _fractionSampledWipe, _fractionSampledHepa, _areaContaminated);
            var analysisCosts = Calculator_analysis.CalculateAnalysisQuantityCost(_fractionSampledWipe, _fractionSampledHepa, _areaContaminated);
            return (suppliesCosts + laborCosts + entExCosts + analysisCosts);
        }

        public CharacterizationSamplingCostCalculator GetCalculator()
        {
            return new CharacterizationSamplingCostCalculator();
        }
    }
}