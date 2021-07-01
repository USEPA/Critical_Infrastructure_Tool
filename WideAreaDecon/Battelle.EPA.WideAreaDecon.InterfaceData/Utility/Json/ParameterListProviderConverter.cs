using System;
using System.Runtime.Serialization;
using Battelle.EPA.WideAreaDecon.InterfaceData.Enumeration.Providers;
using Battelle.EPA.WideAreaDecon.InterfaceData.Interfaces.Providers;
using Battelle.EPA.WideAreaDecon.InterfaceData.Providers;
using Battelle.EPA.WideAreaDecon.InterfaceData.Utility.Extensions;
using Newtonsoft.Json;
using Newtonsoft.Json.Linq;

namespace Battelle.EPA.WideAreaDecon.InterfaceData.Utility.Json
{
    public class ParameterListProviderConverter : JsonConverter
    {
        /// <summary>
        /// Indicates that the item uses the default writer
        /// </summary>
        public override bool CanWrite => false;

        /// <summary>
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
            return objectType == typeof(IParameterListProvider) && objectType.IsInterface;
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
            var jsonObject = JObject.Load(reader);


            //NOTE(quinton): Code here removes case sensitivity;
            //a solution from: https://stackoverflow.com/questions/12055743/json-net-jobject-key-comparison-case-insensitive
            var type = jsonObject
                    .GetValue(nameof(IParameterListProvider.Type), StringComparison.OrdinalIgnoreCase)
                    ?.Value<string>()
                    .ParseEnum<ParameterListProviderType>() ??
                throw new SerializationException("Object did not have required Type selector...");

            return type switch
            {
                ParameterListProviderType.Empty => jsonObject.ToObject<EmptyParameterListProvider>(serializer),
                ParameterListProviderType.ExcelDefineScenario => jsonObject
                    .ToObject<ExcelDefineScenarioParameterListProvider>(serializer),
                ParameterListProviderType.ExcelModifyParameter => jsonObject
                    .ToObject<ExcelModifyParameterParameterListProvider>(serializer),
                _ => throw new SerializationException($"Unknown type {type} found")
            };
        }
    }
}