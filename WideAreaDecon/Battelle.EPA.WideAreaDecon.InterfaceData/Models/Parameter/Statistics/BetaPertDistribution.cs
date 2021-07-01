using System;
using Battelle.EPA.WideAreaDecon.InterfaceData.Enumeration.Parameter;
using Battelle.EPA.WideAreaDecon.InterfaceData.Interfaces.Parameter;
using Battelle.EPA.WideAreaDecon.InterfaceData.Utility.Attributes;
using Battelle.EPA.WideAreaDecon.InterfaceData.Utility.Extensions;
using Battelle.EPA.WideAreaDecon.InterfaceData.Utility.Helpers;
using Battelle.RiskAssessment.Common.Statistics;
using Newtonsoft.Json;
using Newtonsoft.Json.Converters;
using NPOI.SS.UserModel;

namespace Battelle.EPA.WideAreaDecon.InterfaceData.Models.Parameter.Statistics
{
    /// <summary>
    /// Implementation of the beta pert distribution
    /// </summary>
    public class BetaPertDistribution : IParameter
    {
        [JsonConverter(typeof(StringEnumConverter))]
        public ParameterType Type => ParameterType.Pert;

        public ParameterMetaData MetaData { get; set; }

        [JsonProperty(NullValueHandling = NullValueHandling.Ignore)]
        [ExcelProperty(ParameterLocationHelper.Parameter1)]
        public double? Min { get; set; }

        [JsonProperty(NullValueHandling = NullValueHandling.Ignore)]
        [ExcelProperty(ParameterLocationHelper.Parameter2)]
        public double? Max { get; set; }

        [JsonProperty(NullValueHandling = NullValueHandling.Ignore)]
        [ExcelProperty(ParameterLocationHelper.Parameter3)]
        public double? Mode { get; set; }


        public static BetaPertDistribution FromExcel(ParameterMetaData metaData, IRow row)
        {
            var minimum = typeof(BetaPertDistribution).GetCellValue(nameof(Min), row)?.ConvertToOptionalDouble();
            var maximum = typeof(BetaPertDistribution).GetCellValue(nameof(Max), row)?.ConvertToOptionalDouble();
            var mode = typeof(BetaPertDistribution).GetCellValue(nameof(Mode), row)?.ConvertToOptionalDouble();

            if (minimum < metaData.LowerLimit || minimum > metaData.UpperLimit)
            {
                throw new ApplicationException($"Minimum for {metaData.Name} is out of range specified by the lower and upper limit");
            }

            if (maximum < metaData.LowerLimit || maximum > metaData.UpperLimit)
            {
                throw new ApplicationException($"Maximum for {metaData.Name} is out of range specified by the lower and upper limit");
            }

            if (mode < metaData.LowerLimit || mode > metaData.UpperLimit)
            {
                throw new ApplicationException($"Mode for {metaData.Name} is out of range specified by the lower and upper limit");
            }

            return new BetaPertDistribution()
            {
                Min = minimum,
                Max = maximum,
                Mode = mode,
                MetaData = metaData
            };
        }

        public IDistribution CreateDistribution()
        {
            if (Mode.HasValue && Min.HasValue && Max.HasValue)
            {
                return new PertDistribution(Mode.Value, Min.Value, Max.Value);
            }
            throw new ArgumentNullException();
        }

        public string GetTextValue()
        {
            throw new NotImplementedException();
        }
    }
}