import 'reflect-metadata';
import IClientConfiguration from '@/interfaces/configuration/IClientConfiguration';
import { injectable } from 'inversify';
import IClientConfigurationProvider from '@/interfaces/providers/IClientConfigurationProvider';
import ClientConfiguration from '@/store/clientConfiguration/ClientConfiguration';

@injectable()
export default class DefaultClientConfigurationProvider implements IClientConfigurationProvider {
  defaultConfig = new ClientConfiguration();

  // eslint-disable-next-line class-methods-use-this
  async getClientConfigurationAsync(): Promise<IClientConfiguration> {
    return this.getClientConfiguration();
  }

  getClientConfiguration(): IClientConfiguration {
    return this.defaultConfig;
  }
}
