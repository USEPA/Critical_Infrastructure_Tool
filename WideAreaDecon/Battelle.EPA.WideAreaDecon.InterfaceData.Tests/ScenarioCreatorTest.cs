//using System;
//using System.Collections.Generic;
//using System.Text;
//using System.Linq;
//using NUnit.Framework;
//using Battelle.EPA.WideAreaDecon.InterfaceData.Models.Parameter.List;
//using Battelle.EPA.WideAreaDecon.InterfaceData.Providers;
//using Battelle.EPA.WideAreaDecon.InterfaceData.Enumeration.Parameter;
//using Battelle.EPA.WideAreaDecon.InterfaceData.Interfaces.Parameter;

//namespace Battelle.EPA.WideAreaDecon.InterfaceData.Tests
//{
//    public class ScenarioCreatorTests
//    {
//        private ScenarioCreator Creator { get; set; }

//        [SetUp]
//        public void Setup()
//        {
//            string TestFileName1 = @"InputFiles\DefineScenario.xlsx";
//            var defineScenario = new ExcelDefineScenarioParameterListProvider
//            {
//                FileName = TestFileName1
//            };

//            var scenarioDefinition = defineScenario.GetParameterList();

//            var extentOfContaminationParameters = scenarioDefinition.Filters.First(f => f.Name == "Extent of Contamination").Parameters;

//            Creator = new ScenarioCreator(
//                extentOfContaminationParameters.First(p => p.MetaData.Name == "Area Contaminated") as EnumeratedParameter<DecontaminationPhase>,
//                extentOfContaminationParameters.First(p => p.MetaData.Name == "Loading") as EnumeratedParameter<DecontaminationPhase>,
//                extentOfContaminationParameters.First(p => p.MetaData.Name == "Indoor Contamination Breakout") as EnumeratedFraction<BuildingCategory>,
//                extentOfContaminationParameters.First(p => p.MetaData.Name == "Indoor Surface Type Breakout") as EnumeratedFraction<SurfaceType>,
//                extentOfContaminationParameters.First(p => p.MetaData.Name == "Outdoor Surface Type Breakout") as EnumeratedFraction<SurfaceType>,
//                extentOfContaminationParameters.First(p => p.MetaData.Name == "Underground Surface Type Breakout") as EnumeratedFraction<SurfaceType>);
//        }

//        [Test]
//        public void CreateRealizationScenario()
//        {
//            var scenarioDetails = Creator.CreateRealizationScenario();
//        }
//    }
//}
