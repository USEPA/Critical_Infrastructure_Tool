import { injectable } from 'inversify';
import mockDefineScenario from '@/dataMocks/defineParameterMock.json';
import { deserialize } from 'typescript-json-serializer';
import IScenarioParameterProvider from '@/interfaces/providers/IScenarioParameterProvider';
import ParameterList from '../parameter/ParameterList';

@injectable()
export default class DefaultScenarioParameterProvider implements IScenarioParameterProvider {
  data: ParameterList = deserialize<ParameterList>(mockDefineScenario, ParameterList);

  // eslint-disable-next-line class-methods-use-this
  async getScenarioParameters(): Promise<ParameterList> {
    return this.data;
  }
}
