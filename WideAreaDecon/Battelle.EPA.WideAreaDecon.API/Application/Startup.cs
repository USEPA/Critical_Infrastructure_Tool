using System;
using System.IO;
using Battelle.EPA.WideAreaDecon.API.Interfaces;
using Battelle.EPA.WideAreaDecon.InterfaceData.Interfaces;
using Battelle.EPA.WideAreaDecon.InterfaceData.Interfaces.Providers;
using Battelle.EPA.WideAreaDecon.API.Models.ClientConfiguration;
using Battelle.EPA.WideAreaDecon.InterfaceData.Providers;
using Battelle.EPA.WideAreaDecon.API.Services;
using ElectronNET.API;
using Microsoft.AspNetCore.Builder;
using Microsoft.AspNetCore.Hosting;
using Microsoft.AspNetCore.Routing;
using Microsoft.AspNetCore.SpaServices;
using Microsoft.Extensions.Configuration;
using Microsoft.Extensions.DependencyInjection;
using Microsoft.Extensions.Hosting;
using Microsoft.OpenApi.Models;
using Newtonsoft.Json;
using VueCliMiddleware;
using Battelle.EPA.WideAreaDecon.API.Hubs;

namespace Battelle.EPA.WideAreaDecon.API.Application
{
    /// <summary>
    /// The webserver startup options class
    /// </summary>
    public class Startup
    {
        /// <summary>
        /// Constructor which requires a non-null configuration
        /// </summary>
        /// <param name="configuration"></param>
        public Startup(IConfiguration configuration)
        {
            Configuration = configuration ??
                throw new ArgumentNullException(nameof(configuration));
        }

        private IConfiguration Configuration { get; }

        /// <summary>
        /// Called during web host startup to configure the services
        /// </summary>
        /// <param name="services"></param>
        public void ConfigureServices(IServiceCollection services)
        {
            services.AddControllersWithViews()
                .AddNewtonsoftJson();

            services.AddRazorPages();

            // In production, the Vue files will be served from this directory
            services.AddSpaStaticFiles(configuration => { configuration.RootPath = "dist"; });

            // Register the Swagger generator, defining one or more Swagger documents
            services.AddSwaggerGen(c =>
            {
                c.SwaggerDoc(
                    "v1",
                    new OpenApiInfo
                    {
                        Title = "Wide Area Decon Rest API",
                        Version = "v1"
                    });

                c.DocInclusionPredicate((docName, apiDesc) =>
                {
                    if (apiDesc.HttpMethod == null) return false;
                    return true;
                });

                //Set the comments path for the swagger json and ui.
                c.IncludeXmlComments(
                    Path
                        .Combine(
                            AppContext.BaseDirectory,
                            "Battelle.EPA.WideAreaDecon.API.xml"));
            });

            ConfigureModels(services);

            ConfigureProviders(services);
        }

        /// <summary>
        /// This method gets called by the runtime. Use this method to configure the HTTP request pipeline.
        /// </summary>
        /// <param name="app"></param>
        /// <param name="env"></param>
        /// <param name="lifetime"></param>
        public void Configure(IApplicationBuilder app, IWebHostEnvironment env, IHostApplicationLifetime lifetime)
        {
            if (env.IsDevelopment() || HybridSupport.IsElectronActive)
            {
                app.UseDeveloperExceptionPage();
            }
            else
            {
                app.UseExceptionHandler("/Error");
                // The default HSTS value is 30 days. You may want to change this for production scenarios, see https://aka.ms/aspnetcore-hsts.
                app.UseHsts();
                app.UseHttpsRedirection();
            }

            // Enable middleware to serve generated Swagger as a JSON endpoint.
            app.UseSwagger();

            // Enable middleware to serve swagger-ui (HTML, JS, CSS etc.), specifying the Swagger JSON endpoint.
            app.UseSwaggerUI(c => { c.SwaggerEndpoint("/swagger/v1/swagger.json", "Wide Area Decon API V1"); });

            app.UseStaticFiles();
            app.UseSpaStaticFiles();

            ConfigureElectron(
                app, env, lifetime);

            app.UseRouting()
                .UseEndpoints(ConfigureEndpoints);

#if !DEBUG
            app.UseSpa(spa =>
            {
                spa.Options.SourcePath = "dist";
            });
#endif
        }


        private void ConfigureModels(IServiceCollection services)
        {
            services.AddSingleton(Configuration);
            Configuration.GetValue<ClientConfiguration>(nameof(ClientConfiguration));
            services.AddTransient(s =>
                Configuration.GetSection("ClientConfiguration")
                    .Get<ClientConfiguration>());
        }

        private void ConfigureProviders(IServiceCollection services)
        {
            services.AddTransient<
                IClientConfigurationService,
                ClientConfigurationService>();

            services.AddSignalR()
                .AddNewtonsoftJsonProtocol();

            var inputFile = Configuration.GetValue<string>("InputFileConfiguration");

            if (!File.Exists(inputFile))
            {
                throw new ApplicationException($"Could not find input file configuration file: {inputFile}");
            }

            var inputFileConfiguration =
                JsonConvert.DeserializeObject<InputFileConfiguration>(File.ReadAllText(inputFile)) ??
                throw new ApplicationException("Failed to deserialize to input file configuration");

            services.AddSingleton(inputFileConfiguration.ScenarioParameters);
            services.AddSingleton(inputFileConfiguration.BaselineParameters);

            services.AddSingleton<IParameterListProvider>(new EmptyParameterListProvider());

            services.AddSingleton<IJobManager, JobManager>();

            services.AddTransient<JobStatusUpdater>();
            services.AddTransient<JobProgressUpdater>();
        }

        private void ConfigureEndpoints(IEndpointRouteBuilder endpoints)
        {
            endpoints.MapControllerRoute(
                name: "default",
                pattern: "{controller}/{action=Index}/{id?}");

            endpoints.MapHub<JobStatusHub>("/api/job-status-hub");
#if DEBUG
            endpoints.MapToVueCliProxy(
                "{*path}",
                new SpaOptions {SourcePath = "../Battelle.EPA.WideAreaDecon.Client"},
                npmScript: "serve",
                regex: "App running at",
                port: Configuration.GetValue<int>("Port") + 1);
#endif
        }

        private void ConfigureElectron(
            IApplicationBuilder app,
            IWebHostEnvironment env,
            IHostApplicationLifetime lifetime)
        {
            if (HybridSupport.IsElectronActive)
                Configuration.GetSection("ElectronSettings")?
                    .Get<ElectronConfiguration>()?
                    .Configure(app, env, lifetime);
        }
    }
}