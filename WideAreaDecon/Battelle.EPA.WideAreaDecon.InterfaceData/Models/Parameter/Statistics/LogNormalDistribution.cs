using Battelle.EPA.WideAreaDecon.InterfaceData.Enumeration.Parameter;
using Battelle.EPA.WideAreaDecon.InterfaceData.Interfaces.Parameter;
using Battelle.EPA.WideAreaDecon.InterfaceData.Utility.Attributes;
using Battelle.EPA.WideAreaDecon.InterfaceData.Utility.Extensions;
using Battelle.EPA.WideAreaDecon.InterfaceData.Utility.Helpers;
using Newtonsoft.Json;
using Newtonsoft.Json.Converters;
using NPOI.SS.UserModel;
using System;
using Stats = Battelle.RiskAssessment.Common.Statistics;

namespace Battelle.EPA.WideAreaDecon.InterfaceData.Models.Parameter.Statistics
{
    public class LogNormalDistribution : IParameter
    {
        [JsonConverter(typeof(StringEnumConverter))]
        public ParameterType Type => ParameterType.LogNormal;

        public ParameterMetaData MetaData { get; set; }

        [JsonProperty(NullValueHandling = NullValueHandling.Ignore)]
        [ExcelProperty(ParameterLocationHelper.Parameter1)]
        public double? Mean { get; set; }

        [JsonProperty(NullValueHandling = NullValueHandling.Ignore)]
        [ExcelProperty(ParameterLocationHelper.Parameter2)]
        public double? StdDev { get; set; }

        public static LogNormalDistribution FromExcel(ParameterMetaData metaData, IRow information)
        {
            var mean = typeof(LogNormalDistribution).GetCellValue(nameof(Mean), information)?.ConvertToOptionalDouble();

            if (mean < metaData.LowerLimit || mean > metaData.UpperLimit)
            {
                throw new ApplicationException($"Mean for {metaData.Name} is out of range specified by the lower and upper limit");
            }

            return new LogNormalDistribution()
            {
                MetaData = metaData,
                Mean = mean,
                StdDev = typeof(LogNormalDistribution).GetCellValue(nameof(StdDev), information)
                    ?.ConvertToOptionalDouble(),
            };
        }

        public Stats.IDistribution CreateDistribution()
        {
            if (Mean.HasValue && StdDev.HasValue)
            {
                return new Stats.LogNormalDistribution(Mean.Value, StdDev.Value);
            }
            throw new ArgumentNullException();
        }

        public string GetTextValue()
        {
            throw new NotImplementedException();
        }
    }
}