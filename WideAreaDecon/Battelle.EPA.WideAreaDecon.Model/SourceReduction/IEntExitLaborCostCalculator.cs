namespace Battelle.EPA.WideAreaDecon.Model.SourceReduction
{
    public interface IEntExitLaborCostCalculator
    {
        public double CalculateEntExitLaborCost(double workDays, double _numberTeams);
    }
}