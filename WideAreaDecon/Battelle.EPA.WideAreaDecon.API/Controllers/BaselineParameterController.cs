using System;
using System.Collections.Generic;
using System.Linq;
using System.Threading.Tasks;
using Battelle.EPA.WideAreaDecon.InterfaceData.Interfaces.Providers;
using Battelle.EPA.WideAreaDecon.API.Models.ClientConfiguration;
using Battelle.EPA.WideAreaDecon.InterfaceData.Models.Parameter;
using Battelle.EPA.WideAreaDecon.API.Services;
using Microsoft.AspNetCore.Http;
using Microsoft.AspNetCore.Mvc;

namespace Battelle.EPA.WideAreaDecon.API.Controllers
{
    [Route("api/[controller]")]
    [ApiController]
    public class BaselineParameterController : ControllerBase
    {
        private readonly BaselineParameterService _configProvider;

        /// <summary>
        /// Default constructor, requires a non-null provider
        /// </summary>
        /// <param name="configProvider"></param>
        public BaselineParameterController(BaselineParameterService configProvider)
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