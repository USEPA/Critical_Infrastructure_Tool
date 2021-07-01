using System;
using System.Collections.Generic;
using System.Text;

namespace Battelle.EPA.WideAreaDecon.Model
{
    public class CalculatorCreator
    {
        public Services.ICharacterizationSamplingCalculatorFactory _characterizationSamplingFactory;
        public Services.ISourceReductionCalculatorFactory _sourceReductionFactory;
        public Services.IDecontaminationCalculatorFactory _decontaminationFactory;
        public Services.IOtherCalculatorFactory _otherFactory;
        public Services.IIncidentCommandCalculatorFactory _incidentCommandFactory;

        public CalculatorCreator(
            Services.ParameterArrayCharacterizationSamplingCalculatorFactory csCalculatorFactory,
            Services.ParameterArraySourceReductionCalculatorFactory srCalculatorFactory,
            Services.ParameterArrayDecontaminationCalculatorFactory dcCalculatorFactory,
            Services.ParameterArrayOtherCalculatorFactory otCalculatorFactory,
            Services.ParameterArrayIncidentCommandCalculatorFactory icCalculatorFactory)
        {
            _characterizationSamplingFactory = csCalculatorFactory;
            _sourceReductionFactory = srCalculatorFactory;
            _decontaminationFactory = dcCalculatorFactory;
            _otherFactory = otCalculatorFactory;
            _incidentCommandFactory = icCalculatorFactory;
        }

        public ResultsCalculator GetCalculators()
        {
            return new ResultsCalculator(
                _characterizationSamplingFactory.GetCalculator(),
                _sourceReductionFactory.GetCalculator(),
                _decontaminationFactory.GetCalculator(),
                _incidentCommandFactory.GetCalculator(),
                _otherFactory.GetCalculator());
        }
    }
}
