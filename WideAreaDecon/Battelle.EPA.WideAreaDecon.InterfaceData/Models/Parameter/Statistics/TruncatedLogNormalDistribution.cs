using System;
using System.Collections.Generic;
using System.Linq;
using System.Xml.Linq;
using System.Threading.Tasks;
using System.Runtime.Serialization;
using Battelle.EPA.WideAreaDecon.InterfaceData.Enumeration.Parameter;
using Battelle.EPA.WideAreaDecon.InterfaceData.Interfaces.Parameter;
using Battelle.EPA.WideAreaDecon.InterfaceData.Utility.Attributes;
using Battelle.EPA.WideAreaDecon.InterfaceData.Utility.Extensions;
using Battelle.EPA.WideAreaDecon.InterfaceData.Utility.Helpers;
using Newtonsoft.Json;
using Newtonsoft.Json.Converters;
using NPOI.SS.UserModel;
using Stats = Battelle.RiskAssessment.Common.Statistics;

namespace Battelle.EPA.WideAreaDecon.InterfaceData.Models.Parameter.Statistics
{
    /// <summary>
    /// Implementation of the truncated log normal
    /// </summary>
    public class TruncatedLogNormalDistribution : IParameter
    {
        [JsonConverter(typeof(StringEnumConverter))]
        public ParameterType Type => ParameterType.TruncatedLogNormal;

        public ParameterMetaData MetaData { get; set; }

        [JsonProperty(NullValueHandling = NullValueHandling.Ignore)]
        [ExcelProperty(ParameterLocationHelper.Parameter1)]
        public double? Min { get; set; }

        [JsonProperty(NullValueHandling = NullValueHandling.Ignore)]
        [ExcelProperty(ParameterLocationHelper.Parameter2)]
        public double? Max { get; set; }

        [JsonProperty(NullValueHandling = NullValueHandling.Ignore)]
        [ExcelProperty(ParameterLocationHelper.Parameter3)]
        public double? Mean { get; set; }

        [JsonProperty(NullValueHandling = NullValueHandling.Ignore)]
        [ExcelProperty(ParameterLocationHelper.Parameter4)]
        public double? StdDev { get; set; }

        public static TruncatedLogNormalDistribution FromExcel(ParameterMetaData metaData, IRow information)
        {
            var minimum = typeof(TruncatedLogNormalDistribution).GetCellValue(nameof(Min), information)
                    ?.ConvertToOptionalDouble();
            var maximum = typeof(TruncatedLogNormalDistribution).GetCellValue(nameof(Max), information)
                    ?.ConvertToOptionalDouble();
            var mean = typeof(TruncatedLogNormalDistribution).GetCellValue(nameof(Mean), information)
                    ?.ConvertToOptionalDouble();

            if (minimum < metaData.LowerLimit || minimum > metaData.UpperLimit)
            {
                throw new ApplicationException($"Minimum for {metaData.Name} is out of range specified by the lower and upper limit");
            }

            if (maximum < metaData.LowerLimit || maximum > metaData.UpperLimit)
            {
                throw new ApplicationException($"Maximum for {metaData.Name} is out of range specified by the lower and upper limit");
            }

            if (mean < metaData.LowerLimit || mean > metaData.UpperLimit)
            {
                throw new ApplicationException($"Mean for {metaData.Name} is out of range specified by the lower and upper limit");
            }

            return new TruncatedLogNormalDistribution()
            {
                MetaData = metaData,
                Min = minimum,
                Max = maximum,
                Mean = mean,
                StdDev = typeof(TruncatedLogNormalDistribution).GetCellValue(nameof(StdDev), information)
                    ?.ConvertToOptionalDouble(),
            };
        }

        public Stats.IDistribution CreateDistribution()
        {
            if (Min.HasValue && Max.HasValue && Mean.HasValue && StdDev.HasValue)
            {
                return new Stats.TruncatedLogNormalDistribution(Mean.Value, StdDev.Value, Min.Value, Max.Value);
            }
            throw new ArgumentNullException();
        }

        public string GetTextValue()
        {
            throw new NotImplementedException();
        }
    }
}