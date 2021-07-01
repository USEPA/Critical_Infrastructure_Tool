using System;
using System.Collections.Generic;
using System.IO;
using System.Linq;
using System.Reflection;
using System.Runtime.Serialization;
using Battelle.EPA.WideAreaDecon.InterfaceData.Enumeration.Providers;
using Battelle.EPA.WideAreaDecon.InterfaceData.Interfaces.Providers;
using Battelle.EPA.WideAreaDecon.InterfaceData.Models.Parameter;
using Battelle.EPA.WideAreaDecon.InterfaceData.Models.Scenario;
using Newtonsoft.Json;
using Newtonsoft.Json.Converters;
using NPOI.SS.UserModel;
using NPOI.XSSF.UserModel;

namespace Battelle.EPA.WideAreaDecon.InterfaceData.Providers
{
    public class ExcelDefineScenarioParameterListProvider : IParameterListProvider
    {
        [JsonConverter(typeof(StringEnumConverter))]
        public ParameterListProviderType Type => ParameterListProviderType.ExcelDefineScenario;
        public string FileName { get; set; }

        private string FullFileName => Path.Join(
            Path.GetDirectoryName(Assembly.GetExecutingAssembly().Location), FileName);

        public ParameterList GetParameterList()
        {
            if (string.IsNullOrEmpty(FileName))
                throw new ApplicationException(
                    $"No file name provided for {nameof(ExcelDefineScenarioParameterListProvider)}");
            if (!File.Exists(FileName))
            {
                FileName = FullFileName;
                if (!File.Exists(FileName))
                {
                    throw new ApplicationException(
                        $"Could not find {nameof(ExcelDefineScenarioParameterListProvider)} filename: {FileName}");
                }
            }

            // If the file exists, open a new file stream to open the excel workbook
            using var stream = new FileStream(FileName, FileMode.Open, FileAccess.Read) {Position = 0};
            var xssWorkbook = new XSSFWorkbook(stream);

            return ScenarioDefinition.FromExcel(xssWorkbook).GetParameterList();
        }
    }
}