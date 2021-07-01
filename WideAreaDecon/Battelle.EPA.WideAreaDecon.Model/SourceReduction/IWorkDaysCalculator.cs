namespace Battelle.EPA.WideAreaDecon.Model.SourceReduction
{
    public interface IWorkDaysCalculator
    {
        public double CalculateWorkDays(double _numberTeams, double saToBeSourceReduced, double area);
    }
}