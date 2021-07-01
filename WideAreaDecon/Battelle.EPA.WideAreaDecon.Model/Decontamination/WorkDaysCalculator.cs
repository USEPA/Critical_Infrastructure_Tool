using System;
using System.Collections.Generic;
using System.Linq;
using System.Runtime.CompilerServices;
using System.Runtime.Serialization;
using Battelle.EPA.WideAreaDecon.InterfaceData.Enumeration.Parameter;

namespace Battelle.EPA.WideAreaDecon.Model.Decontamination
{
    public class WorkDaysCalculator : IWorkDaysCalculator 
    {
        private readonly Dictionary<SurfaceType, ApplicationMethod> _appMethodBySurfaceType;
        private readonly double _desiredSporeThreshold;
        private readonly Dictionary<ApplicationMethod, double> _treatmentDaysPerAm;
        private readonly IEfficacyCalculator _efficacyCalculator;

        private Dictionary<SurfaceType, double> _surfaceSporeLoading;

        public WorkDaysCalculator(
            Dictionary<SurfaceType, ApplicationMethod> applicationMethods,
            Dictionary<SurfaceType, double> initialSporeLoading,
            double desiredSporeThreshold,
            Dictionary<ApplicationMethod, double> treatmentDaysPerAm,
            IEfficacyCalculator efficacyCalculator)
        {
            _appMethodBySurfaceType = applicationMethods;
            _desiredSporeThreshold = desiredSporeThreshold;
            _treatmentDaysPerAm = treatmentDaysPerAm;
            _efficacyCalculator = efficacyCalculator;
            _surfaceSporeLoading = initialSporeLoading;
        }

        public Tuple<double, int> CalculateWorkDays()
        {
            double totalDays = 0.0;
            int decontaminationRounds = 0;

            while (_surfaceSporeLoading.Values.Any(loading => loading > _desiredSporeThreshold)) {
                var surfaces = _surfaceSporeLoading.Where(pair => pair.Value > _desiredSporeThreshold).Select(pair => pair.Key);
                var methods = _appMethodBySurfaceType.Where(pair => surfaces.Contains(pair.Key)).Select(pair => pair.Value);
                var days = _treatmentDaysPerAm.Where(pair => methods.Contains(pair.Key)).Select(pair => pair.Value);

                totalDays += days.Sum();

                _surfaceSporeLoading = _efficacyCalculator.CalculateEfficacy(_surfaceSporeLoading, _appMethodBySurfaceType);
                decontaminationRounds++;
            }

            Tuple<double, int> decontaminationLabor = new Tuple<double, int>(totalDays, decontaminationRounds);

            return decontaminationLabor;
        }
    }
}