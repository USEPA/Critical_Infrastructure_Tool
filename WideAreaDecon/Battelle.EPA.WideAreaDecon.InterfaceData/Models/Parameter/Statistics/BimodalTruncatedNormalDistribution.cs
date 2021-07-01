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
    /// Implementation of the bimodal truncated normal distribution
    /// </summary>
    public class BimodalTruncatedNormalDistribution : IParameter
    {
        [JsonConverter(typeof(StringEnumConverter))]
        public ParameterType Type => ParameterType.BimodalTruncatedNormal;

        public ParameterMetaData MetaData { get; set; }

        [JsonProperty(NullValueHandling = NullValueHandling.Ignore)]
        [ExcelProperty(ParameterLocationHelper.Parameter1)]
        public double? Mean1 { get; set; }

        [JsonProperty(NullValueHandling = NullValueHandling.Ignore)]
        [ExcelProperty(ParameterLocationHelper.Parameter2)]
        public double? StdDev1 { get; set; }

        [JsonProperty(NullValueHandling = NullValueHandling.Ignore)]
        [ExcelProperty(ParameterLocationHelper.Parameter3)]
        public double? Mean2 { get; set; }

        [JsonProperty(NullValueHandling = NullValueHandling.Ignore)]
        [ExcelProperty(ParameterLocationHelper.Parameter4)]
        public double? StdDev2 { get; set; }

        [JsonProperty(NullValueHandling = NullValueHandling.Ignore)]
        [ExcelProperty(ParameterLocationHelper.Parameter5)]
        public double? Min { get; set; }

        [JsonProperty(NullValueHandling = NullValueHandling.Ignore)]
        [ExcelProperty(ParameterLocationHelper.Parameter6)]
        public double? Max { get; set; }

        public static BimodalTruncatedNormalDistribution FromExcel(ParameterMetaData metaData, IRow information)
        {
            var minimum = typeof(BimodalTruncatedNormalDistribution).GetCellValue(nameof(Min), information)
                    ?.ConvertToOptionalDouble();
            var maximum = typeof(BimodalTruncatedNormalDistribution).GetCellValue(nameof(Max), information)
                    ?.ConvertToOptionalDouble();
            var mean1 = typeof(BimodalTruncatedNormalDistribution).GetCellValue(nameof(Mean1), information)
                    ?.ConvertToOptionalDouble();
            var mean2 = typeof(BimodalTruncatedNormalDistribution).GetCellValue(nameof(Mean2), information)
                    ?.ConvertToOptionalDouble();

            if (minimum < metaData.LowerLimit || minimum > metaData.UpperLimit)
            {
                throw new ApplicationException($"Minimum for {metaData.Name} is out of range specified by the lower and upper limit");
            }

            if (maximum < metaData.LowerLimit || maximum > metaData.UpperLimit)
            {
                throw new ApplicationException($"Maximum for {metaData.Name} is out of range specified by the lower and upper limit");
            }

            if (mean1 < metaData.LowerLimit || mean1 > metaData.UpperLimit)
            {
                throw new ApplicationException($"Mean 1 for {metaData.Name} is out of range specified by the lower and upper limit");
            }

            if (mean2 < metaData.LowerLimit || mean2 > metaData.UpperLimit)
            {
                throw new ApplicationException($"Mean 2 for {metaData.Name} is out of range specified by the lower and upper limit");
            }

            return new BimodalTruncatedNormalDistribution()
            {
                MetaData = metaData,
                Mean1 = mean1,
                StdDev1 = typeof(BimodalTruncatedNormalDistribution).GetCellValue(nameof(StdDev1), information)
                    ?.ConvertToOptionalDouble(),
                Mean2 = mean2,
                StdDev2 = typeof(BimodalTruncatedNormalDistribution).GetCellValue(nameof(StdDev2), information)
                    ?.ConvertToOptionalDouble(),
                Min = minimum,
                Max = maximum,
            };
        }

        public Stats.IDistribution CreateDistribution()
        {
            if (Mean1.HasValue && StdDev1.HasValue && Mean2.HasValue && StdDev2.HasValue && Min.HasValue && Max.HasValue)
            {
                Stats.TruncatedNormalDistribution child1 = new Stats.TruncatedNormalDistribution(Mean1.Value, StdDev1.Value, Min.Value, Max.Value);
                Stats.TruncatedNormalDistribution child2 = new Stats.TruncatedNormalDistribution(Mean2.Value, StdDev2.Value, Min.Value, Max.Value);

                return new Stats.BimodalTruncatedNormalDistribution(child1, child2);
            }
            throw new ArgumentNullException();
        }

        public string GetTextValue()
        {
            throw new NotImplementedException();
        }
    }
}