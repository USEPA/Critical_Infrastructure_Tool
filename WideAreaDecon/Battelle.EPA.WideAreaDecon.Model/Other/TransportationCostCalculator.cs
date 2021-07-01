using System.Collections.Generic;
using System.Linq;
using Battelle.EPA.WideAreaDecon.InterfaceData.Enumeration.Parameter;

namespace Battelle.EPA.WideAreaDecon.Model.Other
{
    public class TransportationCostCalculator : ITransportationCostCalculator
    {
        private readonly double _perDiemCostPerDay;
        private readonly double _personnelPerRentalCar;
        private readonly double _rentalCarCostPerDay;

        public TransportationCostCalculator(
            double personnelPerRentalCar,
            double rentalCarCostPerDay,
            double perDiemCostPerDay)
        {
            _personnelPerRentalCar = personnelPerRentalCar;
            _rentalCarCostPerDay = rentalCarCostPerDay;
            _perDiemCostPerDay = perDiemCostPerDay;
        }

        public double CalculatePerDiem(Dictionary<PersonnelLevel, double> personnelAvailableByType, double totalOnSiteDays)
        {
            var totalPersonnel = personnelAvailableByType.Values.Sum();

            return totalPersonnel * _perDiemCostPerDay * totalOnSiteDays;
        }

        public double CalculateTransportationCost(Dictionary<PersonnelLevel,double> personnelAvailableByType, double personnelRoundTripDays,
            double costPerRoundTripTicket)
        {
            var totalPersonnel = personnelAvailableByType.Values.Sum();

            var rentalCarCost = (totalPersonnel / _personnelPerRentalCar) * _rentalCarCostPerDay * personnelRoundTripDays;

            var airfareCost = totalPersonnel * costPerRoundTripTicket;

            return rentalCarCost + airfareCost;
        }
    }
}