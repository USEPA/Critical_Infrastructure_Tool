using System.Collections.Generic;
using System.Linq;
using Battelle.EPA.WideAreaDecon.InterfaceData.Enumeration.Parameter;

namespace Battelle.EPA.WideAreaDecon.InterfaceData.Models.Parameter
{
    public class CostParameters
    {
        public Dictionary<PersonnelLevel, double> hourlyRate;
        public double icRentalCostPerDay;
        public double icSuppliesCostPerDay;
        public double wipeCost;
        public double hepaCost;
        public double respiratorCost;
        public Dictionary<PpeLevel, double> ppeCost;
        public double wipeAnalysisCost;
        public double hepaAnalysisCost;
        public double vacuumRentalCostPerDay;
        public double costPerMassOfMaterialRemoved;
        public double deconAgentCostPerVolume;
        public double deconMaterialsCost;
        public double rentalCarCostPerDay;
        public double roundtripTicketCostPerPerson;
        public double perDiem;

        public CostParameters(
            Dictionary<PersonnelLevel, double> _hourlyRate,
            double _icRentalCostPerDay,
            double _icSuppliesCostPerDay,
            double _wipeCost,
            double _hepaCost,
            double _respiratorCost,
            Dictionary<PpeLevel, double> _ppeCost,
            double _wipeAnalysisCost,
            double _hepaAnalysisCost,
            double _vacuumRentalCostPerDay,
            double _costPerMassOfMaterialRemoved,
            double _deconAgentCostPerVolume,
            double _deconMaterialsCost,
            double _rentalCarCostPerDay,
            double _roundtripTicketCostPerPerson,
            double _perDiem)
        {
            hourlyRate = _hourlyRate;
            icRentalCostPerDay = _icRentalCostPerDay;
            icSuppliesCostPerDay = _icSuppliesCostPerDay;
            wipeCost = _wipeCost;
            hepaCost = _hepaCost;
            respiratorCost = _respiratorCost;
            ppeCost = _ppeCost;
            wipeAnalysisCost = _wipeAnalysisCost;
            hepaAnalysisCost = _hepaAnalysisCost;
            vacuumRentalCostPerDay = _vacuumRentalCostPerDay;
            costPerMassOfMaterialRemoved = _costPerMassOfMaterialRemoved;
            deconAgentCostPerVolume = _deconAgentCostPerVolume;
            deconMaterialsCost = _deconMaterialsCost;
            rentalCarCostPerDay = _rentalCarCostPerDay;
            roundtripTicketCostPerPerson = _roundtripTicketCostPerPerson;
            perDiem = _perDiem;
        }
    }
}
