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
using Stats = Battelle.RiskAssessment.Common.Statistics;

namespace Battelle.EPA.WideAreaDecon.InterfaceData.Models.Parameter
{
    /// <summary>
    /// Implementation of the text value handling from data sheet
    /// </summary>
    public class TextValue : IParameter
    {
        [JsonConverter(typeof(StringEnumConverter))]
        public ParameterType Type => ParameterType.Text;

        public ParameterMetaData MetaData { get; set; }

        [JsonProperty(NullValueHandling = NullValueHandling.Ignore)]
        [ExcelProperty(ParameterLocationHelper.Parameter1)]
        public string Value { get; set; }

        public static TextValue FromExcel(ParameterMetaData metaData, IRow row)
        {
            var value = typeof(TextValue).GetCellValue(nameof(Value), row);

            return new TextValue()
            {
                Value = value,
                MetaData = metaData
            };
        }

        public Stats.IDistribution CreateDistribution()
        {
            throw new NotImplementedException();
        }

        public string GetTextValue()
        {
            return Value;
        }
    }
}
