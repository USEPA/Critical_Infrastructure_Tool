using System.Collections.Generic;
using System.Linq;
using Battelle.EPA.WideAreaDecon.InterfaceData.Enumeration.Parameter;

namespace Battelle.EPA.WideAreaDecon.Model.Decontamination
{
    public class LaborCostCalculator : ILaborCostCalculator
    {
        private readonly Dictionary<PersonnelLevel, double> _personnelHourlyRate;
        private readonly double _personnelOverhead;
        private readonly Dictionary<PersonnelLevel, double> _personnelReqPerTeam;

        public LaborCostCalculator(
            Dictionary<PersonnelLevel, double> personnelReqPerTeam,
            Dictionary<PersonnelLevel, double> personnelHourlyRate,
            double personnelOverhead,
            IWorkDaysCalculator workDaysCalculator)
        {
            _personnelReqPerTeam = personnelReqPerTeam;
            _personnelHourlyRate = personnelHourlyRate;
            _personnelOverhead = personnelOverhead;
        }

        public double CalculateLaborCost(double workDays, double _numberTeams, double personnelRoundTripDays)
        {
            var personnelHoursCost = _personnelReqPerTeam.Values.Zip(_personnelHourlyRate.Values, (x, y) => x * y).Sum();

            return (workDays + _personnelOverhead) * GlobalConstants.HoursPerWorkDay * _numberTeams * personnelHoursCost;
        }
    }
}