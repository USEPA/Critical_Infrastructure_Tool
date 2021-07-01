using System;
using System.Collections.Generic;
using System.Text;
using Battelle.EPA.WideAreaDecon.InterfaceData.Models.Parameter;
using Battelle.EPA.WideAreaDecon.Model.Services;

namespace Battelle.EPA.WideAreaDecon.Model
{
    public class CalculatorManager
    {
        public CharacterizationSamplingParameters characterizationSamplingParameters;
        public SourceReductionParameters sourceReductionParameters;
        public DecontaminationParameters decontaminationParameters;
        public IncidentCommandParameters incidentCommandParameters;
        public OtherParameters otherParameters;
        public CostParameters costParameters;

        public CalculatorManager(
            CharacterizationSamplingParameters _characterizationSamplingParameters,
            SourceReductionParameters _sourceReductionParameters,
            DecontaminationParameters _decontaminationParameters,
            IncidentCommandParameters _incidentCommandParameters,
            OtherParameters _otherParameters,
            CostParameters _costParameters)
        {
            characterizationSamplingParameters = _characterizationSamplingParameters;
            sourceReductionParameters = _sourceReductionParameters;
            decontaminationParameters = _decontaminationParameters;
            incidentCommandParameters = _incidentCommandParameters;
            otherParameters = _otherParameters;
            costParameters = _costParameters;
        }

        public CalculatorCreator CreateCalculatorFactories()
        {
            var csCalculatorFactory = new ParameterArrayCharacterizationSamplingCalculatorFactory(
                characterizationSamplingParameters,
                costParameters);

            var srCalculatorFactory = new ParameterArraySourceReductionCalculatorFactory(
                sourceReductionParameters,
                costParameters);

            var dcCalculatorFactory = new ParameterArrayDecontaminationCalculatorFactory(
                decontaminationParameters,
                costParameters);

            var otCalculatorFactory = new ParameterArrayOtherCalculatorFactory(
                otherParameters,
                costParameters);

            var icCalculatorFactory = new ParameterArrayIncidentCommandCalculatorFactory(
                characterizationSamplingParameters,
                sourceReductionParameters,
                decontaminationParameters,
                otherParameters,
                incidentCommandParameters,
                costParameters,
                csCalculatorFactory,
                srCalculatorFactory,
                dcCalculatorFactory);

            return new CalculatorCreator(
                csCalculatorFactory,
                srCalculatorFactory,
                dcCalculatorFactory,
                otCalculatorFactory,
                icCalculatorFactory);
        }
    }
}
