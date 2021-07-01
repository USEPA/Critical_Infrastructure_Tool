using Battelle.EPA.WideAreaDecon.Model.CharacterizationSampling;
using System.Collections.Generic;
using Battelle.EPA.WideAreaDecon.InterfaceData.Enumeration.Parameter;
using Battelle.EPA.WideAreaDecon.Model.Services;

namespace Battelle.EPA.WideAreaDecon.Model.SourceReduction
{
    public class SourceReductionCostCalculator : ISourceReductionCalculatorFactory
    {
        public WorkDaysCalculator Calculator_workDays { get; set; }
        public LaborCostCalculator Calculator_labor { get; set; }
        public EntranceExitCostCalculator Calculator_entEx { get; set; }
        public EntExitLaborCostCalculator Calculator_entExLabor { get; set; }

        public double CalculateTime(double _numberTeams, double saToBeSourceReduced, double area)
        {
            return Calculator_workDays.CalculateWorkDays(_numberTeams, saToBeSourceReduced, area);
        }

        public double CalculateCost(double workDays, double _numberTeams, double personnelRoundTripDays, double saToBeSourceReduced, double costPerTonRemoved, Dictionary<PpeLevel, double> ppePerLevelPerTeam, double area)
        {
            var laborCosts = Calculator_labor.CalculateLaborCost(workDays, _numberTeams, saToBeSourceReduced, costPerTonRemoved, area);
            var entExCosts = Calculator_entEx.CalculateEntranceExitCost(workDays, _numberTeams, ppePerLevelPerTeam);
            return (laborCosts + entExCosts);
        }

        public SourceReductionCostCalculator GetCalculator()
        {
            return new SourceReductionCostCalculator();
        }
    }
}