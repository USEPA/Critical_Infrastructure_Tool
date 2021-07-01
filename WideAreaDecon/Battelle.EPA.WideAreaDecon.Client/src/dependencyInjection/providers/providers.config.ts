import { ContainerModule, interfaces } from 'inversify';
import 'reflect-metadata';
import DefaultClientConfigurationProvider from '@/implementations/providers/DefaultClientConfigurationProvider';
import BackendClientConfigurationProvider from '@/implementations/providers/BackendClientConfigurationProvider';
import DefaultNavigationItemProvider from '@/implementations/providers/DefaultNavigationItemProvider';
import DefaultApplicationActionProvider from '@/implementations/providers/DefaultApplicationActionProvider';
import INavigationItemProvider from '@/interfaces/providers/INavigationItemProvider';
import IApplicationActionProvider from '@/interfaces/providers/IApplicationActionProvider';
import IClientConfigurationProvider from '@/interfaces/providers/IClientConfigurationProvider';
import IScenarioDefinitionProvider from '@/interfaces/providers/IScenarioDefinitionProvider';
import DefaultScenarioDefinitionProvider from '@/implementations/providers/DefaultScenarioDefinitionProvider';
import BackendScenarioDefinitionProvider from '@/implementations/providers/BackendScenarioDefinitionProvider';
import IImageProvider from '@/interfaces/providers/IImageProvider';
import DefaultImageProvider from '@/implementations/providers/DefaultImageProvider';
import IHomeOptionsProvider from '@/interfaces/providers/IHomeOptionsProvider';
import DefaultHomeOptionsProvider from '@/implementations/providers/DefaultHomeOptionsProvider';
import IScenarioParameterProvider from '@/interfaces/providers/IScenarioParameterProvider';
import DefaultScenarioParameterProvider from '@/implementations/providers/DefaultScenarioParameterProvider';
import BackendScenarioParameterProvider from '@/implementations/providers/BackendScenarioParameterProvider';
import IDistributionDisplayProvider from '@/interfaces/providers/IDistributionDisplayProvider';
import DistributionDisplayProvider from '@/implementations/providers/DistributionDisplayProvider';
import IJobProvider from '@/interfaces/providers/IJobProvider';
import JobProvider from '@/implementations/providers/JobProvider';
import IJobResultProvider from '@/interfaces/providers/IJobResultProvider';
import JobResultProvider from '@/implementations/providers/JobResultProvider';
import PROVIDER_TYPES from './providers.types';

const providersContainerModule = new ContainerModule((bind: interfaces.Bind) => {
  bind<IClientConfigurationProvider>(PROVIDER_TYPES.ClientConfigurationProvider).to(DefaultClientConfigurationProvider);

  bind<IClientConfigurationProvider>(PROVIDER_TYPES.ClientConfigurationProvider).to(BackendClientConfigurationProvider);

  bind<BackendClientConfigurationProvider>(PROVIDER_TYPES.BackendClientConfigurationProvider).to(
    BackendClientConfigurationProvider,
  );

  bind<INavigationItemProvider>(PROVIDER_TYPES.NavigationItemProvider).to(DefaultNavigationItemProvider);

  bind<IApplicationActionProvider>(PROVIDER_TYPES.ApplicationActionProvider).to(DefaultApplicationActionProvider);

  bind<IScenarioDefinitionProvider>(PROVIDER_TYPES.ScenarioDefinitionProvider).to(DefaultScenarioDefinitionProvider);

  bind<IScenarioDefinitionProvider>(PROVIDER_TYPES.ScenarioDefinitionProvider).to(BackendScenarioDefinitionProvider);

  bind<BackendScenarioDefinitionProvider>(PROVIDER_TYPES.BackendScenarioDefinitionProvider).to(
    BackendScenarioDefinitionProvider,
  );

  bind<IImageProvider>(PROVIDER_TYPES.ImageProvider).to(DefaultImageProvider);

  bind<IHomeOptionsProvider>(PROVIDER_TYPES.HomeOptionsProvider).to(DefaultHomeOptionsProvider);

  bind<IScenarioParameterProvider>(PROVIDER_TYPES.ScenarioParameterProvider).to(DefaultScenarioParameterProvider);

  bind<IScenarioParameterProvider>(PROVIDER_TYPES.ScenarioParameterProvider).to(BackendScenarioParameterProvider);

  bind<BackendScenarioParameterProvider>(PROVIDER_TYPES.BackendScenarioParameterProvider).to(
    BackendScenarioParameterProvider,
  );

  bind<IDistributionDisplayProvider>(PROVIDER_TYPES.DistributionDisplayProvider).to(DistributionDisplayProvider);

  bind<IJobProvider>(PROVIDER_TYPES.JobProvider).to(JobProvider);

  bind<IJobResultProvider>(PROVIDER_TYPES.JobResultProvider).to(JobResultProvider);
});

export default providersContainerModule;
