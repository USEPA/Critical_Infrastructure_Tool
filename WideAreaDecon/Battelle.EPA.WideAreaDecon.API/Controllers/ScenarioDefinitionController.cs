using System;
using Battelle.EPA.WideAreaDecon.API.Models.ClientConfiguration;
using Battelle.EPA.WideAreaDecon.InterfaceData.Models.Parameter;
using Battelle.EPA.WideAreaDecon.API.Services;
using Microsoft.AspNetCore.Mvc;

namespace Battelle.EPA.WideAreaDecon.API.Controllers
{
    [Route("api/[controller]")]
    [ApiController]
    public class ScenarioDefinitionController : ControllerBase
    {
        private readonly ScenarioDefinitionService _configProvider;

        /// <summary>
        /// Default constructor, requires a non-null provider
        /// </summary>
        /// <param name="configProvider"></param>
        public ScenarioDefinitionController(ScenarioDefinitionService configProvider)
        {
            _configProvider = configProvider ??
                throw new ArgumentNullException(nameof(configProvider));
        }

        /// <summary>
        /// Retrieves the client configuration from the backend server
        /// </summary>
        /// <returns>The application configuration for the frontend</returns>
        [HttpGet]
        [ProducesResponseType(typeof(ClientConfiguration), 200)]
        public ParameterList Get()
        {
            return _configProvider.GetParameterList();
        }
    }
}