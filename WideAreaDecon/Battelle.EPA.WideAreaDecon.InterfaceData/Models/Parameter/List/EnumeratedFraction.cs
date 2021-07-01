using System;
using System.Collections.Generic;
using System.Linq;
using Battelle.EPA.WideAreaDecon.InterfaceData.Enumeration.Parameter;
using Battelle.EPA.WideAreaDecon.InterfaceData.Interfaces.Parameter;
using Battelle.EPA.WideAreaDecon.InterfaceData.Models.Parameter.Statistics;
using Battelle.EPA.WideAreaDecon.InterfaceData.Utility.Extensions;
using Microsoft.CodeAnalysis.CSharp.Syntax;
using NPOI.SS.UserModel;
using Battelle.RiskAssessment.Common.Statistics;

namespace Battelle.EPA.WideAreaDecon.InterfaceData.Models.Parameter.List
{
    public class EnumeratedFraction<T> : IParameter where T : Enum
    {
        public ParameterType Type => ParameterType.EnumeratedFraction;
        public string TypeName => typeof(T).Name;
        public ParameterMetaData MetaData { get; set; }

        public Dictionary<T, Statistics.ConstantDistribution> Values { get; set; }

        public static EnumeratedFraction<T> FromExcel(ParameterMetaData metaData, IEnumerable<IRow> rows)
        {
            return new EnumeratedFraction<T>()
            {
                MetaData = metaData,
                Values = rows.ToDictionary(
                    row => ParameterMetaData.FromExcel(row).Category.ParseEnum<T>(),
                    row => Statistics.ConstantDistribution.FromExcel(ParameterMetaData.FromExcel(row), row))
            };
        }

        public IDistribution CreateDistribution()
        {
            throw new NotImplementedException();
        }

        public string GetTextValue()
        {
            throw new NotImplementedException();
        }
    }
}