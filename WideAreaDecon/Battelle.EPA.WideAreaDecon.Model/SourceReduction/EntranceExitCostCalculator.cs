using System.Collections.Generic;
using System.Linq;
using Battelle.EPA.WideAreaDecon.InterfaceData.Enumeration.Parameter;

namespace Battelle.EPA.WideAreaDecon.Model.SourceReduction
{
    public class EntranceExitCostCalculator : IEntranceExitCostCalculator
    {
        private readonly Dictionary<PpeLevel, double> _costPerPpe;
        private readonly double _costPerRespirator;
        private readonly double _numberEntriesPerTeamPerDay;
        private readonly Dictionary<PersonnelLevel, double> _personnelRequiredPerTeam;
        private readonly double _respiratorsPerPerson;

        public EntranceExitCostCalculator(
            Dictionary<PersonnelLevel, double> personnelRequiredPerTeam,
            double numberEntriesPerTeamPerDay,
            double respiratorsPerPerson,
            double costPerRespirator,
            Dictionary<PpeLevel, double> costPerPpe)
        {
            _personnelRequiredPerTeam = personnelRequiredPerTeam;
            _numberEntriesPerTeamPerDay = numberEntriesPerTeamPerDay;
            _respiratorsPerPerson = respiratorsPerPerson;
            _costPerRespirator = costPerRespirator;
            _costPerPpe = costPerPpe;
        }

        public double CalculateEntranceExitCost(double workDays, double _numberTeams, Dictionary<PpeLevel, double> ppePerLevelPerTeam)
        {
            var totalPersonnel = _personnelRequiredPerTeam.Values.Sum() * _numberTeams;
            
            var totalEntries = workDays * _numberEntriesPerTeamPerDay * _numberTeams;

            var totalPpePerLevel = ppePerLevelPerTeam.Values.Select(x => x * _personnelRequiredPerTeam.Values.Sum() * totalEntries);

            var totalCostPpe = totalPpePerLevel.Zip(_costPerPpe.Values, (ppe, cost) => ppe * cost).Sum();

            return (totalPersonnel * _respiratorsPerPerson * _costPerRespirator) + totalCostPpe;
        }
    }
}