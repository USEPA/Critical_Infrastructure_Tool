using Newtonsoft.Json;

namespace Battelle.EPA.WideAreaDecon.API.Models.ClientConfiguration
{
    /// <summary>
    /// Object representing the vuetify theme which is passed to the client application
    /// </summary>
    public class VuetifyTheme
    {
        /// <summary>
        /// Whether or not dark mode should be enabled
        /// </summary>
        [JsonProperty("dark", NullValueHandling = NullValueHandling.Ignore)]
        public bool? DarkModeEnabled { get; set; }

        /// <summary>
        /// Whether or not all themes should be disabled
        /// </summary>
        [JsonProperty("disable", NullValueHandling = NullValueHandling.Ignore)]
        public bool? DisableThemes { get; set; }

        /// <summary>
        /// The color schemes for light and dark which are set
        /// </summary>
        [JsonProperty("themes", NullValueHandling = NullValueHandling.Ignore)]
        public VuetifyColorSchemeMap ColorSchemes { get; set; }
    }
}