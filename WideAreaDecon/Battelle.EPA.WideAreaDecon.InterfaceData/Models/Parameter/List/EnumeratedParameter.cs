using System;
using System.Collections.Generic;
using System.Linq;
using Battelle.EPA.WideAreaDecon.InterfaceData.Enumeration.Parameter;
using Battelle.EPA.WideAreaDecon.InterfaceData.Interfaces.Parameter;
using Battelle.EPA.WideAreaDecon.InterfaceData.Models.Parameter.Statistics;
using Battelle.EPA.WideAreaDecon.InterfaceData.Utility.Extensions;
using NPOI.SS.UserModel;
using Newtonsoft.Json;
using Battelle.EPA.WideAreaDecon.InterfaceData.Utility.Json;
using Battelle.RiskAssessment.Common.Statistics;

namespace Battelle.EPA.WideAreaDecon.InterfaceData.Models.Parameter.List
{
    public class EnumeratedParameter<T> : IParameter where T: struct, Enum
    {
        public ParameterType Type => ParameterType.EnumeratedParameter;
        public string TypeName => typeof(T).Name;
        public ParameterMetaData MetaData { get; set; }
        [JsonProperty(ItemConverterType = typeof(ParameterConverter))]
        public Dictionary<T, IParameter> Values;


        public static EnumeratedParameter<T> FromExcel(ParameterMetaData metaData, IEnumerable<IRow> rows)
        {
            var values = new Dictionary<T, IParameter>();
            foreach (T val in Enum.GetValues(typeof(T)))
            {
                var tRows = rows
                    .Where(row => Enum.Parse<T>(ParameterMetaData.FromExcel(row).Category, true).Equals(val))
                    .ToArray();
                
                if (tRows.Any())
                {
                    if (tRows.Count() == 1)
                    {
                        values[val] = IParameter.FromExcel(ParameterMetaData.FromExcel(tRows[0]), tRows[0]);
                    }
                    else if (tRows.Count() > 1)
                    {
                        values[val] =
                            UniformXDependentDistribution.FromExcel(ParameterMetaData.FromExcel(tRows[0]), tRows); //TODO:: need to figure out name
                    }
                }
            }

            return new EnumeratedParameter<T>()
            {
                MetaData = metaData,
                Values =  values
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