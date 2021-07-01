namespace Battelle.EPA.WideAreaDecon.Model.SourceReduction
{
    public interface ILaborCostCalculator
    {
        public double CalculateLaborCost(double workDays, double _numberTeams, double saToBeSourceReduced, double costPerTonRemoved, double area);
    }
}