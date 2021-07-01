using System;
using Battelle.EPA.WideAreaDecon.API.Interfaces;
using Battelle.EPA.WideAreaDecon.API.Models.ClientConfiguration;
using Microsoft.Extensions.Configuration;

namespace Battelle.EPA.WideAreaDecon.API.Services
{
    /// <summary>
    /// Provides the client HTTP from a config object
    /// </summary>
    public class ClientConfigurationService : IClientConfigurationService
    {
        private readonly IConfiguration _config;

        /// <summary>
        /// Constructs provider with singleton client configuration object
        /// </summary>
        /// <param name="config"></param>
        public ClientConfigurationService(IConfiguration config)
        {
            _config = config ??
                throw new ArgumentNullException(nameof(config));
        }

        /// <summary>
        /// Obtains the configuration
        /// </summary>
        /// <returns></returns>
        public ClientConfiguration GetConfiguration()
        {
            return _config
                .GetSection(nameof(ClientConfiguration))
                .Get<ClientConfiguration>();
        }
    }
}