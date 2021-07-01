using System;

namespace Battelle.EPA.WideAreaDecon.InterfaceData
{
    public class ContaminationInformation
    {
        public ContaminationInformation(double areaContaminated, double loading)
        {
            if (areaContaminated < 0)
            {
                throw new ApplicationException(
                    $"Contamination information {nameof(AreaContaminated)} cannot be less than 0");
            }
            AreaContaminated = areaContaminated;
            Loading = loading;
        }
        public double AreaContaminated { get; set; }
        public double Loading { get; set; }
    }
}