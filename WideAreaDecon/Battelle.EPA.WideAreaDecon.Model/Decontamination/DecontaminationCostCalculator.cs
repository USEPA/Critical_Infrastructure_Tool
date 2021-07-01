using System.Collections.Generic;
using System;
using Battelle.EPA.WideAreaDecon.InterfaceData.Enumeration.Parameter;
using Battelle.EPA.WideAreaDecon.Model.Services;
using Battelle.EPA.WideAreaDecon.InterfaceData;

namespace Battelle.EPA.WideAreaDecon.Model.Decontamination
{
    public class DecontaminationCostCalculator : IDecontaminationCalculatorFactory
    {
        public WorkDaysCalculator Calculator_workDays { get; set; }
        public LaborCostCalculator Calculator_labor { get; set; }
        public SuppliesCostCalculator Calculator_supplies { get; set; }
        public EntranceExitCostCalculator Calculator_entEx { get; set; }

        public Tuple<double, int> CalculateTime()
        {
            return Calculator_workDays.CalculateWorkDays();
        }

        public double CalculateCost(double workDays, double _numberTeams, double personnelRoundTripDays, Dictionary<PpeLevel, double> ppeEachLevelPerTeam, Dictionary<SurfaceType, ContaminationInformation> areaContaminated, Dictionary<SurfaceType, ApplicationMethod> treatmentMethods)
        {
            var suppliesCosts = Calculator_supplies.CalculateSuppliesCost(areaContaminated, treatmentMethods);
            var laborCosts = Calculator_labor.CalculateLaborCost(workDays, _numberTeams, personnelRoundTripDays);
            var entExCosts = Calculator_entEx.CalculateEntranceExitCost(workDays, _numberTeams, ppeEachLevelPerTeam);
            return (suppliesCosts + laborCosts + entExCosts);
        }

        public DecontaminationCostCalculator GetCalculator()
        {
            return new DecontaminationCostCalculator();
        }
    }
}