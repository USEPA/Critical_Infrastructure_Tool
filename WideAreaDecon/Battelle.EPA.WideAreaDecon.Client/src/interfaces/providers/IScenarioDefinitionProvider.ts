import ParameterList from '@/implementations/parameter/ParameterList';

export default interface IScenarioDefinitionProvider {
  getScenarioDefinition(): Promise<ParameterList>;
}
