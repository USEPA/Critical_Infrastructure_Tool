using Battelle.EPA.WideAreaDecon.Model.Other;
using System;
using Battelle.EPA.WideAreaDecon.InterfaceData.Models.Parameter;

namespace Battelle.EPA.WideAreaDecon.Model.Services
{
    /// <summary>
    /// Takes parameter information and generates constructed calculator
    /// </summary>
    public class ParameterArrayOtherCalculatorFactory : IOtherCalculatorFactory
    {
        public TransportationCostCalculator Calculator { get; set; }

        public ParameterArrayOtherCalculatorFactory(
            OtherParameters otherParameters, 
            CostParameters costParameters)
        {
            Calculator = new TransportationCostCalculator(
                otherParameters.personnelPerRentalCar,
                costParameters.rentalCarCostPerDay,
                costParameters.perDiem
            );
        }
        public OtherCostCalculator GetCalculator()
        {
            return new OtherCostCalculator
            {
                Calculator = Calculator
            };
        }
    }
}
