using System.Collections.Generic;
using Battelle.EPA.WideAreaDecon.InterfaceData;
using Battelle.EPA.WideAreaDecon.InterfaceData.Enumeration.Parameter;

namespace Battelle.EPA.WideAreaDecon.Model.IncidentCommand
{
    public class SuppliesCostCalculator : ISuppliesCostCalculator
    {
        private readonly double _equipmentRentalCostPerDay;
        private readonly double _suppliesCostPerDay;

        public SuppliesCostCalculator(
            double equipmentRentalCostPerDay,
            double suppliesCostPerDay)
        {
            _equipmentRentalCostPerDay = equipmentRentalCostPerDay;
            _suppliesCostPerDay = suppliesCostPerDay;
        }

        public double CalculateSuppliesCost(double onSiteDays)
        {
            return onSiteDays * (_equipmentRentalCostPerDay + _suppliesCostPerDay);
        }
    }
}