using System;
using System.Collections.Generic;
using System.Linq;
using Battelle.EPA.WideAreaDecon.InterfaceData.Enumeration.Parameter;
using Battelle.EPA.WideAreaDecon.InterfaceData.Models.Parameter.List;
using Battelle.EPA.WideAreaDecon.InterfaceData.Utility.Extensions;
using Battelle.EPA.WideAreaDecon.InterfaceData.Interfaces.Parameter;

namespace Battelle.EPA.WideAreaDecon.Model.Parameter
{
    public class EfficacyParameterManager
    {
        private readonly Dictionary<SurfaceType, ApplicationMethod> treatmentMethods;
        private readonly IParameter[] efficacyParameters;

        public EfficacyParameterManager(
            Dictionary<SurfaceType, ApplicationMethod> _treatmentMethods,
            IParameter[] _efficacyParameters)
        {
            treatmentMethods = _treatmentMethods;
            efficacyParameters = _efficacyParameters;
        }

        public Dictionary<SurfaceType, double> DrawEfficacyValues()
        {
            var efficacyValues = new Dictionary<SurfaceType, double>();

            foreach (SurfaceType surface in treatmentMethods.Keys.ToList())
            {
                string methodName = treatmentMethods[surface].GetStringValue();
                var metaDataName = methodName + " Efficacy by Surface";
                var values = Enum.GetValues(typeof(ApplicationMethod));

                try
                {
                    var efficacyData = efficacyParameters.First(p => p.MetaData.Name == metaDataName) as EnumeratedParameter<SurfaceType>;

                    if (efficacyData.Values.ContainsKey(surface))
                    {
                        var drawnValue = efficacyData.Values[surface].CreateDistribution().Draw();
                        if (drawnValue < 0)
                        {
                            efficacyValues.Add(surface, 0.0);
                        }
                        else
                        {
                            efficacyValues.Add(surface, drawnValue);
                        }
                    }
                    else
                    {
                        throw new System.InvalidOperationException();
                    }

                }
                catch (System.InvalidOperationException)
                {
                    metaDataName = methodName + " Efficacy";
                    var efficacyData = efficacyParameters.First(p => p.MetaData.Name == metaDataName) as EnumeratedParameter<ApplicationMethod>;

                    var drawnValue = efficacyData.Values[treatmentMethods[surface]].CreateDistribution().Draw();
                    if (drawnValue < 0)
                    {
                        efficacyValues.Add(surface, 0.0);
                    }
                    else
                    {
                        efficacyValues.Add(surface, drawnValue);
                    }
                }
            }

            return efficacyValues;
        }
    }
}
