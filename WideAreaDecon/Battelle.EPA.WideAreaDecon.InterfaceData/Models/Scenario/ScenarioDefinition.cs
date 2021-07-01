using Battelle.EPA.WideAreaDecon.InterfaceData.Models.Parameter;
using NPOI.XSSF.UserModel;

namespace Battelle.EPA.WideAreaDecon.InterfaceData.Models.Scenario
{
    public class ScenarioDefinition
    {
        public ExtentOfContamination Contamination { get; set; }

        public static ScenarioDefinition FromExcel(XSSFWorkbook workbook)
        {
            return new ScenarioDefinition()
            {
                Contamination =  ExtentOfContamination.FromExcel(workbook.GetSheet(ExtentOfContamination.SheetName))
            };
        }

        public ParameterList GetParameterList()
        {
            return new ParameterList()
            {
                Filters = new[]
                {
                    Contamination.GetParameterFilter()
                }
            };
        }
    }
}