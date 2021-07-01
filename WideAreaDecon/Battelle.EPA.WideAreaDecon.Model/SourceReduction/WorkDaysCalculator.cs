namespace Battelle.EPA.WideAreaDecon.Model.SourceReduction
{
    public class WorkDaysCalculator : IWorkDaysCalculator
    {
        private readonly double _massPerSa;
        private readonly double _massRemovedPerHrPerTeam;

        public WorkDaysCalculator(
            double massRemovedPerHrPerTeam,
            double massPerSa)
        {
            _massRemovedPerHrPerTeam = massRemovedPerHrPerTeam;
            _massPerSa = massPerSa;
        }

        public double CalculateWorkDays(double _numberTeams, double saToBeSourceReduced, double area)
        {
            return (saToBeSourceReduced * area) * _massPerSa / (GlobalConstants.HoursPerWorkDay * _massRemovedPerHrPerTeam * _numberTeams);
        }
    }
}