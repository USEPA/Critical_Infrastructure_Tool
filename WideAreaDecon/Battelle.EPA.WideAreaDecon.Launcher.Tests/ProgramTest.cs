using NUnit.Framework;
using Newtonsoft.Json;
using System.IO;
using Battelle.EPA.WideAreaDecon.InterfaceData.Models.Parameter;

namespace Battelle.EPA.WideAreaDecon.Launcher.Tests
{
    public class ProgramTest
    {
        [SetUp]
        public void Setup()
        {
            
        }

        [Test]
        public void JsonSerializer()
        {
            var path = @"..\\netcoreapp3.1\\InputFiles\\DEFINE.json";
            string json = File.ReadAllText(path);

            ParameterList scenarioDetails = JsonConvert.DeserializeObject<ParameterList>(json);

            Assert.Pass();
        }
    }
}