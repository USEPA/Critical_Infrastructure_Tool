using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Runtime.Serialization;
using System.Xml.Linq;
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
    /// Implementation fo the constant distribution
    /// </summary>
    public class ConstantDistribution : IParameter
    {
        [JsonConverter(typeof(StringEnumConverter))]
        public ParameterType Type => ParameterType.Constant;

        [JsonProperty(NullValueHandling = NullValueHandling.Ignore)]
        [ExcelProperty(ParameterLocationHelper.Parameter1)]
        public double? Value { get; set; }

        public ParameterMetaData MetaData { get; set; }

        public static ConstantDistribution FromExcel(ParameterMetaData metaData, IRow row)
        {
            var value = typeof(ConstantDistribution).GetCellValue(nameof(Value), row)?.ConvertToOptionalDouble();

            if (value < metaData.LowerLimit || value > metaData.UpperLimit)
            {
                throw new ApplicationException($"Value for {metaData.Name} is out of range specified by the lower and upper limit");
            }

            return new ConstantDistribution()
            {
                Value = value,
                MetaData = metaData
            };
        }

        public Stats.IDistribution CreateDistribution()
        {
            if (Value.HasValue)
            {
                return new Stats.ConstantDistribution(Value.Value);
            }
            throw new ArgumentNullException();
        }

        public string GetTextValue()
        {
            throw new NotImplementedException();
        }
    }
}