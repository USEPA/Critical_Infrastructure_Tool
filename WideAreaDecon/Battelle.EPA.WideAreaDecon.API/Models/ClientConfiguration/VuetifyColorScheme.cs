using System.Drawing;
using Battelle.EPA.WideAreaDecon.InterfaceData.Utility.Json;
using Newtonsoft.Json;

namespace Battelle.EPA.WideAreaDecon.API.Models.ClientConfiguration
{
    /// <summary>
    /// Object containing the vuetify color scheme settings
    /// </summary>
    public class VuetifyColorScheme
    {
        /// <summary>
        /// The primary color
        /// </summary>
        [JsonConverter(typeof(NewtonsoftJsonColorConverter))]
        [JsonProperty("primary", NullValueHandling = NullValueHandling.Ignore)]
        public Color? Primary { get; set; }

        /// <summary>
        /// The secondary color
        /// </summary>
        [JsonConverter(typeof(NewtonsoftJsonColorConverter))]
        [JsonProperty("secondary", NullValueHandling = NullValueHandling.Ignore)]
        public Color? Secondary { get; set; }

        /// <summary>
        /// The accent color
        /// </summary>
        [JsonConverter(typeof(NewtonsoftJsonColorConverter))]
        [JsonProperty("accent", NullValueHandling = NullValueHandling.Ignore)]
        public Color? Accent { get; set; }

        /// <summary>
        /// The info color
        /// </summary>
        [JsonConverter(typeof(NewtonsoftJsonColorConverter))]
        [JsonProperty("info", NullValueHandling = NullValueHandling.Ignore)]
        public Color? Info { get; set; }

        /// <summary>
        /// The warning color
        /// </summary>
        [JsonConverter(typeof(NewtonsoftJsonColorConverter))]
        [JsonProperty("warning", NullValueHandling = NullValueHandling.Ignore)]
        public Color? Warning { get; set; }

        /// <summary>
        /// The error color
        /// </summary>
        [JsonConverter(typeof(NewtonsoftJsonColorConverter))]
        [JsonProperty("error", NullValueHandling = NullValueHandling.Ignore)]
        public Color? Error { get; set; }

        /// <summary>
        /// The success color
        /// </summary>
        [JsonConverter(typeof(NewtonsoftJsonColorConverter))]
        [JsonProperty("success", NullValueHandling = NullValueHandling.Ignore)]
        public Color? Success { get; set; }

        /// <summary>
        /// The anchor color
        /// </summary>
        [JsonConverter(typeof(NewtonsoftJsonColorConverter))]
        [JsonProperty("anchor", NullValueHandling = NullValueHandling.Ignore)]
        public Color? Anchor { get; set; }
    }
}