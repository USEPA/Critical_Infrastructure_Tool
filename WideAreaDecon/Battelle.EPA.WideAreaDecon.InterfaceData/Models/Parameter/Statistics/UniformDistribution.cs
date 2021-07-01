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
    /// Implementation for the uniform distribution
    /// </summary>
    public class UniformDistribution : IParameter
    {
        [JsonConverter(typeof(StringEnumConverter))]
        public ParameterType Type => ParameterType.Uniform;

        public ParameterMetaData MetaData { get; set; }

        [JsonProperty(NullValueHandling = NullValueHandling.Ignore)]
        [ExcelProperty(ParameterLocationHelper.Parameter1)]
        public double? Min { get; set; }

        [JsonProperty(NullValueHandling = NullValueHandling.Ignore)]
        [ExcelProperty(ParameterLocationHelper.Parameter2)]
        public double? Max { get; set; }


        public static UniformDistribution FromExcel(ParameterMetaData metaData, IRow information)
        {
            var minimum = typeof(UniformDistribution).GetCellValue(nameof(Min), information)?.ConvertToOptionalDouble();
            var maximum = typeof(UniformDistribution).GetCellValue(nameof(Max), information)?.ConvertToOptionalDouble();

            if (minimum < metaData.LowerLimit || minimum > metaData.UpperLimit)
            {
                throw new ApplicationException($"Minimum for {metaData.Name} is out of range specified by the lower and upper limit");
            }

            if (maximum < metaData.LowerLimit || maximum > metaData.UpperLimit)
            {
                throw new ApplicationException($"Maximum for {metaData.Name} is out of range specified by the lower and upper limit");
            }

            return new UniformDistribution()
            {
                MetaData = metaData,
                Min = minimum,
                Max = maximum
            };
        }

        public Stats.IDistribution CreateDistribution()
        {
            if (Min.HasValue && Max.HasValue)
            {
                return new Stats.UniformDistribution(Min.Value, Max.Value);
            }
            throw new ArgumentNullException();
        }

        public string GetTextValue()
        {
            throw new NotImplementedException();
        }
    }
}