using System;
using System.Linq;
using System.Collections.Generic;
using Battelle.EPA.WideAreaDecon.InterfaceData;
using Battelle.EPA.WideAreaDecon.InterfaceData.Enumeration.Parameter;

namespace Battelle.EPA.WideAreaDecon.Model.CharacterizationSampling
{
    public class SuppliesCostCalculator : ISuppliesCostCalculator
    {
        private readonly double _costPerVacuum;
        private readonly double _costPerWipe;
        private readonly double _hepaRentalCostPerDay;
        private readonly double _hepaSocksPerHourPerTeam;
        private readonly double _surfaceAreaPerHepaSock;
        private readonly double _surfaceAreaPerWipe;
        private readonly double _wipesPerHourPerTeam;

        public SuppliesCostCalculator(
            double surfaceAreaPerWipe,
            double surfaceAreaPerHepaSock,
            double wipesPerHourPerTeam,
            double hepaSocksPerHourPerTeam,
            double costPerWipe,
            double costPerVacuum,
            double hepaRentalCostPerDay)
        {
            _surfaceAreaPerWipe = surfaceAreaPerWipe;
            _surfaceAreaPerHepaSock = surfaceAreaPerHepaSock;
            _wipesPerHourPerTeam = wipesPerHourPerTeam;
            _hepaSocksPerHourPerTeam = hepaSocksPerHourPerTeam;
            _costPerWipe = costPerWipe;
            _costPerVacuum = costPerVacuum;
            _hepaRentalCostPerDay = hepaRentalCostPerDay;
        }

        public double CalculateSuppliesCost(double _numberTeams, double _fractionSampledWipe, double _fractionSampledHepa, Dictionary<SurfaceType, ContaminationInformation> _areaContaminated)
        {
            var contaminationArea = new Dictionary<SurfaceType, double>();
            foreach (SurfaceType surface in _areaContaminated.Keys.ToList())
            {
                contaminationArea.Add(surface, _areaContaminated[surface].AreaContaminated);
            }
            var surfaceAreaToBeWiped = _fractionSampledWipe * contaminationArea.Values.Sum();
            var surfaceAreaToBeHepa = _fractionSampledHepa * contaminationArea.Values.Sum();

            return surfaceAreaToBeWiped / _surfaceAreaPerWipe * _costPerWipe +
                surfaceAreaToBeHepa / _surfaceAreaPerHepaSock * _costPerVacuum + surfaceAreaToBeHepa /
                _surfaceAreaPerHepaSock / (_hepaSocksPerHourPerTeam * _numberTeams * GlobalConstants.HoursPerWorkDay) * _hepaRentalCostPerDay;
        }

        public double CalculateWorkDays(double _numberTeams, double _fractionSampledWipe, double _fractionSampledHepa, Dictionary<SurfaceType, ContaminationInformation> _areaContaminated)
        {
            var contaminationArea = new Dictionary<SurfaceType, double>();
            foreach (SurfaceType surface in _areaContaminated.Keys.ToList())
            {
                contaminationArea.Add(surface, _areaContaminated[surface].AreaContaminated);
            }
            var surfaceAreaToBeWiped = _fractionSampledWipe * contaminationArea.Values.Sum();
            var surfaceAreaToBeHepa = _fractionSampledHepa * contaminationArea.Values.Sum();

            return Math.Abs(surfaceAreaToBeWiped / _surfaceAreaPerWipe / (_wipesPerHourPerTeam * _numberTeams) / GlobalConstants.HoursPerWorkDay) +
                Math.Abs(surfaceAreaToBeHepa / _surfaceAreaPerHepaSock / (_hepaSocksPerHourPerTeam * _numberTeams) /
                    GlobalConstants.HoursPerWorkDay);
        }
    }
}