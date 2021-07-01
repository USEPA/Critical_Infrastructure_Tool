import 'reflect-metadata';
import IClientConfiguration from '@/interfaces/configuration/IClientConfiguration';
import { injectable } from 'inversify';
import IClientConfigurationProvider from '@/interfaces/providers/IClientConfigurationProvider';

import axios from 'axios';

@injectable()
export default class BackendClientConfigurationProvider implements IClientConfigurationProvider {
  // eslint-disable-next-line class-methods-use-this
  getClientConfigurationAsync(): Promise<IClientConfiguration> {
    return axios
      .get<IClientConfiguration>('/api/ClientConfiguration')
      .then<IClientConfiguration>((response) => response.data);
  }
}
