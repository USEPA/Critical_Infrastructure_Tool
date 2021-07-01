using Newtonsoft.Json;

namespace Battelle.EPA.WideAreaDecon.API.Models.ClientConfiguration
{
    /// <summary>
    /// Mapping object representing the Vuetify color scheme
    /// </summary>
    public class VuetifyColorSchemeMap
    {
        /// <summary>
        /// The light scheme settings
        /// </summary>
        [JsonProperty("light", NullValueHandling = NullValueHandling.Ignore)]
        public VuetifyColorScheme LightScheme { get; set; }

        /// <summary>
        /// The dark scheme settings
        /// </summary>
        [JsonProperty("dark", NullValueHandling = NullValueHandling.Ignore)]
        public VuetifyColorScheme DarkScheme { get; set; }
    }
}