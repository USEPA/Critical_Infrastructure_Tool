using System.Collections.Generic;
using System;
using System.Linq;
using Battelle.EPA.WideAreaDecon.InterfaceData.Enumeration.Parameter;
using Battelle.EPA.WideAreaDecon.InterfaceData;

namespace Battelle.EPA.WideAreaDecon.Model.CharacterizationSampling
{
    public class AnalysisQuantityCostCalculator : IAnalysisQuantityCostCalculator
    {
        private readonly double _costPerHepaAnalysis;
        private readonly double _costPerWipeAnalysis;
        private readonly double _surfaceAreaPerHepaSock;
        private readonly double _surfaceAreaPerWipe;

        public AnalysisQuantityCostCalculator(double surfaceAreaPerWipe, double surfaceAreaPerHepaSock, double costPerWipeAnalysis,
            double costPerHepaAnalysis)
        {
            _surfaceAreaPerWipe = surfaceAreaPerWipe;
            _surfaceAreaPerHepaSock = surfaceAreaPerHepaSock;
            _costPerWipeAnalysis = costPerWipeAnalysis;
            _costPerHepaAnalysis = costPerHepaAnalysis;
        }

        public double CalculateAnalysisQuantityCost(double _fractionSampledWipe, double _fractionSampledHepa, Dictionary<SurfaceType, ContaminationInformation> _areaContaminated)
        {
            var contaminationArea = new Dictionary<SurfaceType, double>();
            foreach (SurfaceType surface in _areaContaminated.Keys.ToList())
            {
                contaminationArea.Add(surface, _areaContaminated[surface].AreaContaminated);
            }
            var surfaceAreaToBeWiped = _fractionSampledWipe * contaminationArea.Values.Sum();
            var surfaceAreaToBeHepa = _fractionSampledHepa * contaminationArea.Values.Sum();

            return surfaceAreaToBeWiped / _surfaceAreaPerWipe * _costPerWipeAnalysis +
                surfaceAreaToBeHepa / _surfaceAreaPerHepaSock * _costPerHepaAnalysis;
        }
    }
}