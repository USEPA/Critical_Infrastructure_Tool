const PROVIDER_TYPES = {
  ClientConfigurationProvider: Symbol('IClientConfigurationProvider'),
  BackendClientConfigurationProvider: Symbol('BackendClientConfigurationProvider'),
  NavigationItemProvider: Symbol('INavigationItemProvider'),
  ApplicationActionProvider: Symbol('IApplicationActionProvider'),
  ScenarioDefinitionProvider: Symbol('IScenarioDefinitionProvider'),
  ImageProvider: Symbol('IImageProvider'),
  HomeOptionsProvider: Symbol('IHomeOptionsProvider'),
  ScenarioParameterProvider: Symbol('IScenarioParameterProvider'),
  BackendScenarioDefinitionProvider: Symbol('BackendScenarioDefinitionProvider'),
  BackendScenarioParameterProvider: Symbol('BackendScenarioParameterProvider'),
  DistributionDisplayProvider: Symbol('DistributionDisplayProvider'),
  JobProvider: Symbol('IJobProvider'),
  JobResultProvider: Symbol('IJobResultProvider'),
};

export default PROVIDER_TYPES;
