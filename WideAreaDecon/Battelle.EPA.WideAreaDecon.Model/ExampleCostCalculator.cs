namespace Battelle.EPA.WideAreaDecon.Model
{
    public class ExampleCostCalculator
    {
        public ExampleCostCalculator(double someParameter1, double someParameter2)
        {
            SomeParameter1 = someParameter1;
            SomeParameter2 = someParameter2;
        }

        private double SomeParameter1 { get; }
        private double SomeParameter2 { get; }

        public double CalculateCost(double someOtherInput1)
        {
            return (SomeParameter1 + SomeParameter2) * someOtherInput1;
        }
    }
}