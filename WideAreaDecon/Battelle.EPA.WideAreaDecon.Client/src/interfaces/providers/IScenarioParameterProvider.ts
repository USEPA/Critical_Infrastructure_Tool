import ParameterList from '@/implementations/parameter/ParameterList';

export default interface IScenarioParameterProvider {
  getScenarioParameters(): Promise<ParameterList>;
}
