using System;

namespace Battelle.EPA.WideAreaDecon.Model.Decontamination
{
    public interface IWorkDaysCalculator
    {
        public Tuple<double, int> CalculateWorkDays();
    }
}