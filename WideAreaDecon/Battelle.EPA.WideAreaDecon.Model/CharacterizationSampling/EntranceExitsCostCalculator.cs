using System.Collections.Generic;
using System.Linq;
using Battelle.EPA.WideAreaDecon.InterfaceData;
using Battelle.EPA.WideAreaDecon.InterfaceData.Enumeration.Parameter;

namespace Battelle.EPA.WideAreaDecon.Model.CharacterizationSampling
{
    public class EntrancesExitsCostCalculator : IEntrancesExitsCostCalculator
    {
        private readonly Dictionary<PpeLevel, double> _costPerPpe;
        private readonly double _costPerRespirator;

        private readonly ILaborCostCalculator _laborCostCalculator;
        private readonly Dictionary<PersonnelLevel, double> _personnelRequiredPerTeam;
        private readonly double _respiratorsPerPerson;
        private readonly double _numberEntriesPerTeamPerDay;

        private readonly ISuppliesCostCalculator _suppliesCostCalculator;

        public EntrancesExitsCostCalculator(
            Dictionary<PersonnelLevel, double> personnelRequiredPerTeam,
            double numberEntriesPerTeamPerDay,
            double respiratorsPerPerson,
            double costPerRespirator,
            Dictionary<PpeLevel, double> costPerPpe,
            ILaborCostCalculator laborCostCalculator,
            ISuppliesCostCalculator suppliesCostCalculator)
        {
            _personnelRequiredPerTeam = personnelRequiredPerTeam;
            _numberEntriesPerTeamPerDay = numberEntriesPerTeamPerDay;
            _respiratorsPerPerson = respiratorsPerPerson;
            _costPerRespirator = costPerRespirator;
            _costPerPpe = costPerPpe;
            _laborCostCalculator = laborCostCalculator;
            _suppliesCostCalculator = suppliesCostCalculator;
        }

        public double CalculateEntrancesExitsCost(double workDays, double _numberTeams, Dictionary<PpeLevel, double> ppePerLevelPerTeam, double _fractionSampledWipe, double _fractionSampledHepa, Dictionary<SurfaceType, ContaminationInformation> _areaContaminated)
        {
            var totalPersonnel = _personnelRequiredPerTeam.Values.Sum() * _numberTeams;

            var totalEntries = workDays * _numberEntriesPerTeamPerDay * _numberTeams;

            var totalPpePerLevel = ppePerLevelPerTeam.Values.Select(x => x * _personnelRequiredPerTeam.Values.Sum() * totalEntries);

            var totalCostPpe = totalPpePerLevel.Zip(_costPerPpe.Values, (ppe, cost) => ppe * cost).Sum();

            return (totalPersonnel * _respiratorsPerPerson * _costPerRespirator) + totalCostPpe;
        }
    }
}