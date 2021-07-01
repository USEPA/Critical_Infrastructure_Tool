using System.Threading.Tasks;
using ElectronNET.API;
using ElectronNET.API.Entities;
using Microsoft.AspNetCore.Builder;
using Microsoft.AspNetCore.Hosting;
using Microsoft.Extensions.Hosting;

namespace Battelle.EPA.WideAreaDecon.API.Application
{
    /// <summary>
    /// Object representing the electron configuration settings
    /// </summary>
    public class ElectronConfiguration
    {
        private BrowserWindowOptions WindowOptions { get; }

        /// <summary>
        /// Default constructor, instantiates a default browser window
        /// </summary>
        public ElectronConfiguration()
        {
            WindowOptions = new BrowserWindowOptions()
            {
                Title = "Wide Area Decontamination Tool",
                AutoHideMenuBar = true,
                Width = 1920,
                Height = 1080
            };
        }

        /// <summary>
        /// Configures the application to start for the given app, environment and lifetime
        /// </summary>
        /// <param name="app"></param>
        /// <param name="env"></param>
        /// <param name="lifetime"></param>
        public void Configure(
            IApplicationBuilder app,
            IWebHostEnvironment env,
            IHostApplicationLifetime lifetime)
        {
            StartWindow(lifetime);
        }

        private void StartWindow(
            IHostApplicationLifetime lifetime)
        {
            // Open the Electron-Window here
            Task.Run(async () =>
            {
                var browserWindow =
                    await Electron.WindowManager.CreateWindowAsync(WindowOptions ?? new BrowserWindowOptions());
                browserWindow.Maximize();
                Electron.GlobalShortcut.Register("CommandOrControl+Shift+I",
                    () => { browserWindow.WebContents.OpenDevTools(); });
                browserWindow.OnClose += lifetime.StopApplication;
            });
        }
    }
}