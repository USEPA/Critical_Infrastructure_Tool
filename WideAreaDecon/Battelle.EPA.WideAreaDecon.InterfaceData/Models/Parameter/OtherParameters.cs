using System;
using System.Collections.Generic;
using System.Linq;
using Battelle.EPA.WideAreaDecon.InterfaceData.Enumeration.Parameter;

namespace Battelle.EPA.WideAreaDecon.InterfaceData.Models.Parameter
{
    public class OtherParameters
    {
        public double personnelPerRentalCar;
        public double roundtripDays;
        public Dictionary<PersonnelLevel, double> totalAvailablePersonnel;

        public OtherParameters(
            double _personnelPerRentalCar,
            double _roundtripDays,
            Dictionary<PersonnelLevel, double> _totalAvailablePersonnel)
        {
            personnelPerRentalCar = _personnelPerRentalCar;
            roundtripDays = _roundtripDays;
            totalAvailablePersonnel = _totalAvailablePersonnel;
        }
    }
}
