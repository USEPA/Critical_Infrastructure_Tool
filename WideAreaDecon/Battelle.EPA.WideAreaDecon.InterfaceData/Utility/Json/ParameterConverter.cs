using System;
using System.Runtime.Serialization;
using Battelle.EPA.WideAreaDecon.InterfaceData.Enumeration.Parameter;
using Battelle.EPA.WideAreaDecon.InterfaceData.Interfaces.Parameter;
using Battelle.EPA.WideAreaDecon.InterfaceData.Models.Parameter;
using Battelle.EPA.WideAreaDecon.InterfaceData.Models.Parameter.Statistics;
using Battelle.EPA.WideAreaDecon.InterfaceData.Models.Parameter.List;
using Battelle.EPA.WideAreaDecon.InterfaceData.Utility.Extensions;
using Newtonsoft.Json;
using Newtonsoft.Json.Linq;

namespace Battelle.EPA.WideAreaDecon.InterfaceData.Utility.Json
{
    public class ParameterConverter : JsonConverter
    {
        /// <summary>
        /// Indicates that the item uses the default writer
        /// </summary>
        public override bool CanWrite => false;

        // <summary>
        /// Indicates that the item uses a custom reader
        /// </summary>
        public override bool CanRead => true;

        /// <summary>
        /// Checks if the object can be converted
        /// </summary>
        /// <param name="objectType">The type of object to check</param>
        /// <returns>True if the type is DynamicParameterData</returns>
        public override bool CanConvert(Type objectType)
        {
            return objectType == typeof(IParameter) && objectType.IsInterface;
        }

        /// <summary>
        /// Do not use, use default
        /// </summary>
        /// <param name="writer"></param>
        /// <param name="value"></param>
        /// <param name="serializer"></param>
        public override void WriteJson(JsonWriter writer,
            object value, JsonSerializer serializer)
        {
            throw new InvalidOperationException("Use default serialization.");
        }

        /// <summary>
        /// Reads the json data object into a DynamicParameterData
        /// </summary>
        /// <param name="reader">The reader</param>
        /// <param name="objectType">The object type</param>
        /// <param name="existingValue">The existing value</param>
        /// <param name="serializer">The serializer</param>
        /// <returns></returns>
        public override object ReadJson(JsonReader reader,
            Type objectType, object existingValue,
            JsonSerializer serializer)
        {
            var JsonObject = JObject.Load(reader);

            //NOTE(quinton): Code here removes case sensitivity;
            //a solution from: https://stackoverflow.com/questions/12055743/json-net-jobject-key-comparison-case-insensitive
            var type = JsonObject
                    .GetValue(nameof(IParameter.Type), StringComparison.OrdinalIgnoreCase)
                    ?.Value<string>()
                    .ParseEnum<ParameterType>() ??
                throw new SerializationException("Object did not have required Type selector...");

            return type switch
            {
                ParameterType.BimodalTruncatedNormal => JsonObject.ToObject<BimodalTruncatedNormalDistribution>(serializer),
                ParameterType.Constant => JsonObject.ToObject<ConstantDistribution>(serializer),
                ParameterType.EnumeratedFraction => GetEnumeratedFractionFromJson(JsonObject, serializer),
                ParameterType.EnumeratedParameter => GetEnumeratedParameterFromJson(JsonObject, serializer),
                ParameterType.LogNormal => JsonObject.ToObject<LogNormalDistribution>(),
                ParameterType.LogUniform => JsonObject.ToObject<LogUniformDistribution>(),
                ParameterType.Pert => JsonObject.ToObject<BetaPertDistribution>(),
                ParameterType.TruncatedLogNormal => JsonObject.ToObject<TruncatedNormalDistribution>(),
                ParameterType.TruncatedNormal => JsonObject.ToObject<TruncatedNormalDistribution>(),
                ParameterType.Uniform => JsonObject.ToObject<UniformDistribution>(),
                ParameterType.UniformXDependent => JsonObject.ToObject<UniformXDependentDistribution>(),
                ParameterType.Weibull => JsonObject.ToObject<WeibullDistribution>(),
                ParameterType.Text => JsonObject.ToObject<TextValue>(),
                _ => throw new SerializationException($"Unknown type {type} found")
            };
        }

        private object GetEnumeratedParameterFromJson(JObject JsonObject, JsonSerializer serializer)
        {
            var typeName = JsonObject
                    .GetValue("typeName", StringComparison.OrdinalIgnoreCase)
                    ?.Value<string>() ??
                    throw new SerializationException("Enumerated parameter did not have required type name");

            return typeName switch
            {
                "DecontaminationPhase" => JsonObject.ToObject<EnumeratedParameter<DecontaminationPhase>>(serializer),
                "ApplicationMethod" => JsonObject.ToObject<EnumeratedParameter<ApplicationMethod>>(serializer),
                "SurfaceType" => JsonObject.ToObject<EnumeratedParameter<SurfaceType>>(serializer),
                _ => throw new SerializationException($"Uknown enumerated parameter type name {typeName} found")
            };

        }

        private object GetEnumeratedFractionFromJson(JObject JsonObject, JsonSerializer serializer)
        {
            var typeName = JsonObject
                    .GetValue("typeName", StringComparison.OrdinalIgnoreCase)
                    ?.Value<string>() ??
                    throw new SerializationException("Enumerated fraction did not have required type name");

            return typeName switch
            {
                "BuildingCategory" => JsonObject.ToObject<EnumeratedFraction<BuildingCategory>>(serializer),
                "SurfaceType" => JsonObject.ToObject<EnumeratedFraction<SurfaceType>>(serializer),
                _ => throw new SerializationException($"Uknown enumerated fraction type name {typeName} found")
            };

        }
    }
}
