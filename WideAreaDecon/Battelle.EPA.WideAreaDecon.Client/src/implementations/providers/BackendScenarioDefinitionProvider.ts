import { injectable } from 'inversify';
import IScenarioDefinitionProvider from '@/interfaces/providers/IScenarioDefinitionProvider';
import { deserialize } from 'typescript-json-serializer';
import axios from 'axios';

import ParameterList from '../parameter/ParameterList';

@injectable()
export default class DefaultScenarioDefinitionProvider implements IScenarioDefinitionProvider {
  // eslint-disable-next-line class-methods-use-this
  async getScenarioDefinition(): Promise<ParameterList> {
    return axios
      .get<ParameterList>('/api/ScenarioDefinition')
      .then<ParameterList>((response) => deserialize<ParameterList>(response.data, ParameterList));
  }
}
