using System;
using System.Drawing;
using Newtonsoft.Json;
using Newtonsoft.Json.Linq;

namespace Battelle.EPA.WideAreaDecon.InterfaceData.Utility.Json
{
    /// <summary>
    /// A converter which converts C# Color objects to Hex strings
    /// </summary>
    public class NewtonsoftJsonColorConverter : JsonConverter
    {
        /// <summary>
        /// Writes the color to the provided json writer
        /// </summary>
        /// <param name="writer"></param>
        /// <param name="value"></param>
        /// <param name="serializer"></param>
        public override void WriteJson(JsonWriter writer, object value, JsonSerializer serializer)
        {
            if (!(value is Color castColor))
            {
                throw new ArgumentException("Color converter can only handle Color types!");
            }

            JToken
                .FromObject($"#{castColor.R:X2}{castColor.G:X2}{castColor.B:X2}")
                .WriteTo(writer);
        }

        /// <summary>
        /// No implemented because CanRead is set to false
        /// </summary>
        /// <param name="reader"></param>
        /// <param name="objectType"></param>
        /// <param name="existingValue"></param>
        /// <param name="serializer"></param>
        /// <returns></returns>
        public override object ReadJson(JsonReader reader, Type objectType, object existingValue,
            JsonSerializer serializer) =>
            throw new NotImplementedException(
                "Unnecessary because CanRead is false. The type will skip the converter.");

        /// <summary>
        /// Set to false because colors don't need a custom serializer
        /// </summary>
        public override bool CanRead => false;

        /// <summary>
        /// Indicates that any object of type Color can be converted
        /// </summary>
        /// <param name="objectType"></param>
        /// <returns></returns>
        public override bool CanConvert(Type objectType) => objectType == typeof(Color);
    }
}