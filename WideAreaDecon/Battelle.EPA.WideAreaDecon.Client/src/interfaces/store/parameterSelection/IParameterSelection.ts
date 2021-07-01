import ParameterWrapper from '@/implementations/parameter/ParameterWrapper';
import IDefineScenarioSelection from './IDefineScenarioSelection';
import IScenarioParameterSelection from './IScenarioParameterSelection';

export default interface IParameterSelection extends IDefineScenarioSelection, IScenarioParameterSelection {
  currentSelectedParameter: ParameterWrapper;
}
