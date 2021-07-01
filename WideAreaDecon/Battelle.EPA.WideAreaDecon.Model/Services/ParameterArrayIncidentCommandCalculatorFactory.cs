using Battelle.EPA.WideAreaDecon.Model.IncidentCommand;
using System;
using System.Collections.Generic;
using Battelle.EPA.WideAreaDecon.InterfaceData.Models.Parameter;

namespace Battelle.EPA.WideAreaDecon.Model.Services
{
    /// <summary>
    /// Takes parameter information and generates constructed calculator
    /// </summary>
    public class ParameterArrayIncidentCommandCalculatorFactory : IIncidentCommandCalculatorFactory
    {
        public LaborCostCalculator Calculator_labor { get; set; }
        public SuppliesCostCalculator Calculator_supplies { get; set; }
        public CharacterizationSampling.LaborCostCalculator Calculator_laborCs { get; set; }
        public CharacterizationSampling.PhaseLagCalculator Calculator_phaseLag { get; set; }
        public CharacterizationSampling.SuppliesCostCalculator Calculator_suppliesCs { get; set; }
        public SourceReduction.LaborCostCalculator Calculator_laborSr { get; set; }
        public SourceReduction.WorkDaysCalculator Calculator_workDaysSr { get; set; }
        public Decontamination.LaborCostCalculator Calculator_laborDc { get; set; }
        public Decontamination.EfficacyCalculator Calculator_efficacy { get; set; }
        public Decontamination.WorkDaysCalculator Calculator_workDaysDc { get; set; }

        public ParameterArrayIncidentCommandCalculatorFactory(
            CharacterizationSamplingParameters csParameters,
            SourceReductionParameters srParameters,
            DecontaminationParameters dcParameters,
            OtherParameters otParameters,
            IncidentCommandParameters icParameters,
            CostParameters costParameters,
            ParameterArrayCharacterizationSamplingCalculatorFactory csParameterArray,
            ParameterArraySourceReductionCalculatorFactory srParameterArray,
            ParameterArrayDecontaminationCalculatorFactory dcParameterArray)
        {
            Calculator_phaseLag = new CharacterizationSampling.PhaseLagCalculator(
                csParameters.surfaceAreaPerWipe,
                csParameters.surfaceAreaPerHepa,
                csParameters.labUptimesHours,
                csParameters.samplePackageTime,
                csParameters.labDistanceFromSite,
                csParameters.labThroughput
            );

            Calculator_suppliesCs = new CharacterizationSampling.SuppliesCostCalculator(
                csParameters.surfaceAreaPerWipe,
                csParameters.surfaceAreaPerHepa,
                csParameters.wipesPerHrPerTeam,
                csParameters.hepaSocksPerHrPerTeam,
                costParameters.wipeCost,
                costParameters.hepaCost,
                costParameters.vacuumRentalCostPerDay
            );

            Calculator_laborCs = new CharacterizationSampling.LaborCostCalculator(
                csParameters.personnelReqPerTeam,
                csParameters.personnelOverheadDays,
                csParameters.entriesPerTeam,
                csParameters.hoursEntering,
                csParameters.hoursExiting,
                costParameters.hourlyRate,
                Calculator_suppliesCs,
                Calculator_phaseLag
            );
            
            Calculator_workDaysSr = new SourceReduction.WorkDaysCalculator(
                srParameters.massRemovedPerHourPerTeam,
                srParameters.massPerSurfaceArea
            );

            Calculator_laborSr = new SourceReduction.LaborCostCalculator(
                srParameters.personnelOverheadDays,
                srParameters.personnelReqPerTeam,
                costParameters.hourlyRate,
                srParameters.massPerSurfaceArea,
                Calculator_workDaysSr
            );

            Calculator_efficacy = new Decontamination.EfficacyCalculator(
                dcParameters.efficacyParameters
            );

            Calculator_workDaysDc = new Decontamination.WorkDaysCalculator(
                dcParameters.applicationMethods,
                dcParameters.initialSporeLoading,
                dcParameters.desiredSporeThreshold,
                dcParameters.treatmentDaysPerAm,
                Calculator_efficacy
            );

            Calculator_laborDc = new Decontamination.LaborCostCalculator(
                dcParameters.personnelReqPerTeam,
                costParameters.hourlyRate,
                dcParameters.personnelOverhead,
                Calculator_workDaysDc
            );

            Calculator_labor = new LaborCostCalculator(
                icParameters.personnelReqPerTeam,
                icParameters.personnelOverheadDays,
                costParameters.hourlyRate,
                Calculator_laborCs,
                Calculator_phaseLag,
                Calculator_laborSr,
                Calculator_laborDc
            );

            Calculator_supplies = new SuppliesCostCalculator(
                costParameters.icRentalCostPerDay,
                costParameters.icSuppliesCostPerDay
            );
        }

        public IncidentCommandCostCalculator GetCalculator()
        {
            return new IncidentCommandCostCalculator
            {
                Calculator_labor = Calculator_labor,
                Calculator_supplies = Calculator_supplies,
                Calculator_laborCs = Calculator_laborCs,
                Calculator_phaseLag = Calculator_phaseLag,
                Calculator_suppliesCs = Calculator_suppliesCs,
                Calculator_laborSr = Calculator_laborSr,
                Calculator_workDaysSr = Calculator_workDaysSr,
                Calculator_laborDc = Calculator_laborDc,
                Calculator_efficacy = Calculator_efficacy,
                Calculator_workDaysDc = Calculator_workDaysDc
            };
        }
    }
}
