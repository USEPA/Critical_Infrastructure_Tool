using System.Collections.Generic;
using System.Linq;
using Battelle.EPA.WideAreaDecon.InterfaceData.Enumeration.Parameter;
using Battelle.EPA.WideAreaDecon.InterfaceData;

namespace Battelle.EPA.WideAreaDecon.Model.CharacterizationSampling
{
    public class LaborCostCalculator : ILaborCostCalculator
    {
        private readonly double _hoursPerEntryPerTeam;
        private readonly double _hoursPerExitPerTeam;
        private readonly double _numberEntriesPerTeamPerDay;
        private readonly Dictionary<PersonnelLevel, double> _personnelHourlyRate;
        private readonly double _personnelOverhead;
        private readonly Dictionary<PersonnelLevel, double> _personnelRequiredPerTeam;

        private readonly ISuppliesCostCalculator _suppliesCostCalculator;

        private readonly IPhaseLagCalculator _phaseLagCalculator;

        public LaborCostCalculator(
            Dictionary<PersonnelLevel, double> personnelRequiredPerTeam,
            double personnelOverhead,
            double numberEntriesPerTeamPerDay,
            double hoursPerEntryPerTeam,
            double hoursPerExitPerTeam,
            Dictionary<PersonnelLevel, double> personnelHourlyRate,
            ISuppliesCostCalculator suppliesCostCalculator,
            IPhaseLagCalculator phaseLagCalculator)
        {
            _personnelRequiredPerTeam = personnelRequiredPerTeam;
            _personnelOverhead = personnelOverhead;
            _numberEntriesPerTeamPerDay = numberEntriesPerTeamPerDay;
            _hoursPerEntryPerTeam = hoursPerEntryPerTeam;
            _hoursPerExitPerTeam = hoursPerExitPerTeam;
            _personnelHourlyRate = personnelHourlyRate;
            _suppliesCostCalculator = suppliesCostCalculator;
            _phaseLagCalculator = phaseLagCalculator;
        }
        
        public double CalculateLaborCost(double workDays, double _numberTeams, double _personnelRoundTripDays, double _fractionSampledWipe, double _fractionSampledHepa, Dictionary<SurfaceType, ContaminationInformation> _areaContaminated)
        {
            var personnelHoursCost = _personnelRequiredPerTeam.Values.Zip(_personnelHourlyRate.Values, (x, y) => x * y).Sum();

            return (workDays + _personnelOverhead) * GlobalConstants.HoursPerWorkDay * _numberTeams * personnelHoursCost;
        }

        public double CalculateLaborDays(double workDays)
        {
            return workDays + _personnelOverhead;
        }
    }
}