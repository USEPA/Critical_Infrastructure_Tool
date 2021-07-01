using System.Collections.Generic;

namespace Battelle.EPA.WideAreaDecon.Model.Decontamination
{
    public interface ILaborCostCalculator
    {
        public double CalculateLaborCost(double workDays, double _numberTeams, double personnelRoundTripDays);
    }
}