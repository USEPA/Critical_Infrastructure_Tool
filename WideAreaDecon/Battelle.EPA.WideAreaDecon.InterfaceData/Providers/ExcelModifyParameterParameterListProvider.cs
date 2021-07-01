using System;
using System.Collections.Generic;
using System.IO;
using System.Linq;
using System.Reflection;
using System.Runtime.Serialization;
using Battelle.EPA.WideAreaDecon.InterfaceData.Enumeration.Parameter;
using Battelle.EPA.WideAreaDecon.InterfaceData.Enumeration.Providers;
using Battelle.EPA.WideAreaDecon.InterfaceData.Interfaces.Parameter;
using Battelle.EPA.WideAreaDecon.InterfaceData.Interfaces.Providers;
using Battelle.EPA.WideAreaDecon.InterfaceData.Models.Parameter;
using Battelle.EPA.WideAreaDecon.InterfaceData.Models.Parameter.List;
using Battelle.EPA.WideAreaDecon.InterfaceData.Utility.Extensions;
using Microsoft.OpenApi.Extensions;
using Newtonsoft.Json;
using Newtonsoft.Json.Converters;
using NPOI.SS.UserModel;
using NPOI.XSSF.UserModel;

namespace Battelle.EPA.WideAreaDecon.InterfaceData.Providers
{
    public class ExcelModifyParameterParameterListProvider : IParameterListProvider
    {
        [JsonConverter(typeof(StringEnumConverter))]
        public ParameterListProviderType Type => ParameterListProviderType.ExcelModifyParameter;

        public string FileName { get; set; }

        private string FullFileName => Path.Join(
            Path.GetDirectoryName(Assembly.GetExecutingAssembly().Location), FileName);

        public string[] GenericSheetNames { get; set; }

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
            XSSFWorkbook xssWorkbook = new XSSFWorkbook(stream);

            // Building Treatment Methods Enumerated Parameter
            var treatmentMethods = new List<IParameter>();
            var treatmentMethodSheet = xssWorkbook.GetSheet("Decon Methods by Surface");
            var row = new Dictionary<IRow, ParameterMetaData>();

            for (var i = 1; i <= treatmentMethodSheet.LastRowNum; i++)
            {
                row.Add(treatmentMethodSheet.GetRow(i), ParameterMetaData.FromExcel(treatmentMethodSheet.GetRow(i)));
            }

            treatmentMethods.Add(EnumeratedParameter<SurfaceType>.FromExcel(new ParameterMetaData()
            {
                Name = "Decontamination Method by Surface",
                Description = "The decontamination methods to be applied to each surface",
            }, row.Select(row => row.Key)));

            // Building Efficacy Enumerated Parameters
            var efficacyParameters = new List<IParameter>();
            foreach (var method in Enum.GetValues(typeof(ApplicationMethod)).Cast<ApplicationMethod>())
            {
                var methodSheet = xssWorkbook.GetSheet(method.GetStringValue());
                var rows = new Dictionary<IRow, ParameterMetaData>();
                for (var i = 1; i <= methodSheet.LastRowNum; i++)
                {
                    rows.Add(methodSheet.GetRow(i), ParameterMetaData.FromExcel(methodSheet.GetRow(i)));
                }

                var surfaceCategory = rows.Where(row =>
                    Enum.TryParse(typeof(SurfaceType), row.Value.Category, true, out var tmp)).ToArray();
                if (surfaceCategory.Any())
                {
                    efficacyParameters.Add(EnumeratedParameter<SurfaceType>.FromExcel(new ParameterMetaData()
                    {
                        Name = $"{method.GetStringValue()} Efficacy by Surface",
                        Description = $"The Efficacy of {method.GetStringValue()} based on the surface it is applied to",
                        Units = "log reduction",
                    }, surfaceCategory.Select(row => row.Key)));
                }

                var methodCategory = rows.Where(row => Enum.TryParse(typeof(ApplicationMethod),
                    ParameterMetaData.FromExcel(row.Key).Category,
                    true,
                    out var tmp)).ToArray();
                if (methodCategory.Any())
                {
                    efficacyParameters.Add(EnumeratedParameter<ApplicationMethod>.FromExcel(new ParameterMetaData()
                    {
                        Name = $"{method.GetStringValue()} Efficacy",
                        Description = $"The Efficacy of {method.GetStringValue()} independent of the surface it is applied to",
                        Units = "log reduction",
                    }, methodCategory.Select(row => row.Key)));
                }
            }

            var filters = GenericSheetNames.Select(genericSheetName =>
                ParameterFilter.FromExcelSheet(xssWorkbook.GetSheet(genericSheetName))).ToList();
            filters.Add(new ParameterFilter()
            {
                Name = "Efficacy",
                Filters = new ParameterFilter[0],
                Parameters = efficacyParameters.ToArray()
            });
            filters.Add(new ParameterFilter()
            {
                Name = "Decontamination Treatment Methods by Surface",
                Filters = new ParameterFilter[0],
                Parameters = treatmentMethods.ToArray()
            });


            return new ParameterList()
            {
                Filters = filters.ToArray()
            };
        }
    }
}