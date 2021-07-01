using Battelle.EPA.WideAreaDecon.Model.Decontamination;
using System;
using Battelle.EPA.WideAreaDecon.InterfaceData.Models.Parameter;

namespace Battelle.EPA.WideAreaDecon.Model.Services
{
    /// <summary>
    /// Takes parameter information and generates constructed calculator
    /// </summary>
    public class ParameterArrayDecontaminationCalculatorFactory : IDecontaminationCalculatorFactory
    {
        public SuppliesCostCalculator Calculator_supplies { get; set; }
        public LaborCostCalculator Calculator_labor { get; set; }
        public WorkDaysCalculator Calculator_workDays { get; set; }
        public EntranceExitCostCalculator Calculator_entEx { get; set; }
        public EfficacyCalculator Calculator_efficacy { get; set; }

        public ParameterArrayDecontaminationCalculatorFactory(
            DecontaminationParameters dcParameters, 
            CostParameters costParameters)
        {
            Calculator_efficacy = new EfficacyCalculator(
                dcParameters.efficacyParameters
            );

            Calculator_workDays = new WorkDaysCalculator(
                dcParameters.applicationMethods,
                dcParameters.initialSporeLoading,
                dcParameters.desiredSporeThreshold,
                dcParameters.treatmentDaysPerAm,
                Calculator_efficacy
            );

            Calculator_supplies = new SuppliesCostCalculator(
                costParameters.deconAgentCostPerVolume,
                costParameters.deconMaterialsCost,
                dcParameters.fumigationAgentVolume,
                dcParameters.agentVolume
            );

            Calculator_labor = new LaborCostCalculator(
                dcParameters.personnelReqPerTeam,
                costParameters.hourlyRate,
                dcParameters.personnelOverhead,
                Calculator_workDays
            );

            Calculator_entEx = new EntranceExitCostCalculator(
                dcParameters.personnelReqPerTeam,
                dcParameters.numEntriesPerTeamPerDay,
                dcParameters.respiratorsPerPerson,
                costParameters.respiratorCost,
                costParameters.ppeCost
            );
        }
        public DecontaminationCostCalculator GetCalculator()
        {
            return new DecontaminationCostCalculator
            {
                Calculator_workDays = Calculator_workDays,
                Calculator_supplies = Calculator_supplies,
                Calculator_labor = Calculator_labor,
                Calculator_entEx = Calculator_entEx
            };
        }
    }
}
