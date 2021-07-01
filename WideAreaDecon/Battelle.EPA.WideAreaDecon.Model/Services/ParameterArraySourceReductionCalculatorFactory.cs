using Battelle.EPA.WideAreaDecon.Model.SourceReduction;
using System;
using Battelle.EPA.WideAreaDecon.InterfaceData.Models.Parameter;

namespace Battelle.EPA.WideAreaDecon.Model.Services
{
    /// <summary>
    /// Takes parameter information and generates constructed calculator
    /// </summary>
    public class ParameterArraySourceReductionCalculatorFactory : ISourceReductionCalculatorFactory
    {
        public LaborCostCalculator Calculator_labor { get; set; }
        public WorkDaysCalculator Calculator_workDays { get; set; }
        public EntranceExitCostCalculator Calculator_entEx { get; set; }
        public EntExitLaborCostCalculator Calculator_entExLabor { get; set; }

        public ParameterArraySourceReductionCalculatorFactory(
            SourceReductionParameters srParameters,
            CostParameters costParameters)
        {
            Calculator_workDays = new WorkDaysCalculator(
                srParameters.massRemovedPerHourPerTeam,
                srParameters.massPerSurfaceArea
            );

            Calculator_labor = new LaborCostCalculator(
                srParameters.personnelOverheadDays,
                srParameters.personnelReqPerTeam,
                costParameters.hourlyRate,
                srParameters.massPerSurfaceArea,
                Calculator_workDays
            );

            Calculator_entExLabor = new EntExitLaborCostCalculator(
                srParameters.personnelReqPerTeam,
                costParameters.hourlyRate,
                srParameters.numEntriesPerDay,
                srParameters.hoursEntering,
                srParameters.hoursExiting,
                Calculator_workDays
            );

            Calculator_entEx = new EntranceExitCostCalculator(
                srParameters.personnelReqPerTeam,
                srParameters.numEntriesPerDay,
                srParameters.respiratorsPerPerson,
                costParameters.respiratorCost,
                costParameters.ppeCost
            );
        }
        public SourceReductionCostCalculator GetCalculator()
        {
            return new SourceReductionCostCalculator
            {
                Calculator_workDays = Calculator_workDays,
                Calculator_labor = Calculator_labor,
                Calculator_entEx = Calculator_entEx,
                Calculator_entExLabor = Calculator_entExLabor
            };
        }
    }
}
