using System.Collections.Generic;
using System.Linq;
using Battelle.EPA.WideAreaDecon.InterfaceData.Enumeration.Parameter;

namespace Battelle.EPA.WideAreaDecon.Model.Other
{
    public interface ITransportationCostCalculator
    {
        public double CalculatePerDiem(Dictionary<PersonnelLevel, double> personnelAvailableByType, double totalOnSiteDays);

        public double CalculateTransportationCost(Dictionary<PersonnelLevel, double> personnelAvailableByType, double personnelRoundTripDays,
            double costPerRoundTripTicket);
    }
}