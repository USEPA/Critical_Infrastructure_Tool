using System;
using Battelle.EPA.WideAreaDecon.API.Application;
using ElectronNET.API;
using Microsoft.AspNetCore;
using Microsoft.AspNetCore.Hosting;
using Microsoft.AspNetCore.Server.Kestrel.Core;
using Microsoft.Extensions.Configuration;
using Microsoft.Extensions.DependencyInjection;
using Battelle.EPA.WideAreaDecon.API.Interfaces;
using Battelle.EPA.WideAreaDecon.API.Services;

namespace Battelle.EPA.WideAreaDecon.API
{
    /// <summary>
    /// Entry point class for the application
    /// </summary>
    public static class Program
    {
        /// <summary>
        /// The entry point application, starts the program
        /// </summary>
        /// <param name="args">The argument list - utilized in electron settings</param>
        public static void Main(string[] args) => WebHost
                .CreateDefaultBuilder<Startup>(args)
                .ConfigureAppConfiguration(ConfigureIfElectron)
                .ConfigureKestrel(ConfigureConfigureKestrelSettings)
                .UseElectron(args)
                .Build()
                .Run();

        private static void ConfigureConfigureKestrelSettings(WebHostBuilderContext ctx, KestrelServerOptions serverOptions)
        {
            var port = HybridSupport.IsElectronActive
                ? Convert.ToInt32(BridgeSettings.WebPort)
                : ctx.Configuration.GetValue<int>("Port");

            serverOptions.ListenLocalhost(port);
        }


        private static void ConfigureIfElectron(WebHostBuilderContext context, IConfigurationBuilder builder)
        {
            if (!HybridSupport.IsElectronActive)
                return;

            context.HostingEnvironment.EnvironmentName = "Electron";
            builder.AddJsonFile($"appsettings.Electron.json", true);
            Environment.SetEnvironmentVariable("ASPNETCORE_ENVIRONMENT", "Electron", EnvironmentVariableTarget.Process);
        }
    }
}
