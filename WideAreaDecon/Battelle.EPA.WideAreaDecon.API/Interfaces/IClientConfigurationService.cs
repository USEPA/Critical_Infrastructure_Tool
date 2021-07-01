using Battelle.EPA.WideAreaDecon.API.Models.ClientConfiguration;

namespace Battelle.EPA.WideAreaDecon.API.Interfaces
{
    /// <summary>
    /// Provides a client configuration object
    /// </summary>
    public interface IClientConfigurationService
    {
        /// <summary>
        /// Gets the client configuration
        /// </summary>
        /// <returns></returns>
        ClientConfiguration GetConfiguration();
    }
}