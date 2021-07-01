using System;
using System.Collections.Generic;
using System.Linq;
using Battelle.EPA.WideAreaDecon.InterfaceData;
using Battelle.EPA.WideAreaDecon.InterfaceData.Enumeration.Parameter;

namespace Battelle.EPA.WideAreaDecon.Model.CharacterizationSampling
{
    public class PhaseLagCalculator : IPhaseLagCalculator
    {
        private readonly double _surfaceAreaPerWipe;
        private readonly double _surfaceAreaPerHepa;
        private readonly double _samplePackageTime;
        private readonly List<double> _labUptimesHours;
        private readonly List<double> _labDistanceFromSite;
        private readonly List<double> _labThroughput;

        public PhaseLagCalculator(
            double surfaceAreaPerWipe,  
            double surfaceAreaPerHepa, 
            List<double> labUptimesHours, 
            double samplePackageTime,
            List<double> labDistanceFromSite,
            List<double> labThroughput)
        {
            _surfaceAreaPerWipe = surfaceAreaPerWipe;
            _surfaceAreaPerHepa = surfaceAreaPerHepa;
            _labUptimesHours = labUptimesHours;
            _samplePackageTime = samplePackageTime;
            _labDistanceFromSite = labDistanceFromSite;
            _labThroughput = labThroughput;
        }

        public double CalculatePhaseLagTime(int numberLabs, double sampleTimeTransmitted, double _fractionSampledWipe, double _fractionSampledHepa, Dictionary<SurfaceType, ContaminationInformation> _areaContaminated)
        {
            var contaminationArea = new Dictionary<SurfaceType, double>();
            foreach (SurfaceType surface in _areaContaminated.Keys.ToList())
            {
                contaminationArea.Add(surface, _areaContaminated[surface].AreaContaminated);
            }
            var surfaceAreaToBeWiped = _fractionSampledWipe * contaminationArea.Values.Sum();
            var surfaceAreaToBeHepa = _fractionSampledHepa * contaminationArea.Values.Sum();

            double totalWipes = (surfaceAreaToBeWiped / _surfaceAreaPerWipe);
            double totalHepa = (surfaceAreaToBeHepa / _surfaceAreaPerHepa);

            double wipesPerLab = totalWipes / numberLabs;
            double hepaPerLab = totalHepa / numberLabs;

            double maxLabTime = 0;

            double[] shippingTimePerLab = new double[numberLabs], analysisTimePerLab = new double[numberLabs];

            for (int i = 0; i < numberLabs; i++)
            {
                shippingTimePerLab[i] = _labDistanceFromSite[i] / (GlobalConstants.HoursPerWorkDay * GlobalConstants.AssumedDriverSpeed);

                analysisTimePerLab[i] = (wipesPerLab + hepaPerLab) / _labThroughput[i];

                if ((analysisTimePerLab[i] + shippingTimePerLab[i]) > maxLabTime)
                {
                    maxLabTime = (analysisTimePerLab[i] + shippingTimePerLab[i]);
                }
            }

            double totalPackagingTime = (_samplePackageTime * (totalHepa + totalWipes)) / (GlobalConstants.MinutesToHours * GlobalConstants.HoursPerWorkDay);

            return totalPackagingTime + maxLabTime + (sampleTimeTransmitted / GlobalConstants.HoursPerWorkDay);
        }
    }
}