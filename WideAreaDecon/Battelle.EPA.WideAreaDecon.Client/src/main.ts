import 'core-js/stable';
import 'regenerator-runtime/runtime';
import Vue from 'vue';
import '@/plugins/axios';
import GetVuetify from '@/plugins/vuetify';
import App from '@/components/App.vue';
import router from '@/router';
import store from '@/store/index';
import '@fortawesome/fontawesome-free/css/all.css';
import BackendClientConfigurationProvider from '@/implementations/providers/BackendClientConfigurationProvider';
import container from '@/dependencyInjection/config';
import TYPES from '@/dependencyInjection/types';
// eslint-disable-next-line @typescript-eslint/no-unused-vars
import * as _ from 'lodash';
import IScenarioDefinitionProvider from './interfaces/providers/IScenarioDefinitionProvider';
import DefaultClientConfigurationProvider from './implementations/providers/DefaultClientConfigurationProvider';
import IApplicationActionProvider from './interfaces/providers/IApplicationActionProvider';
import INavigationItemProvider from './interfaces/providers/INavigationItemProvider';
import IScenarioParameterProvider from './interfaces/providers/IScenarioParameterProvider';
import ParameterList from './implementations/parameter/ParameterList';
import ParameterSelection from './store/parameterSelection/ParameterSelection';

Vue.config.productionTip = false;

let defaultConfig = new DefaultClientConfigurationProvider().getClientConfiguration();
let defaultScenario: ParameterList;
let defaultParameters: ParameterList;

const clientConfigPromise = container
  .get<BackendClientConfigurationProvider>(TYPES.BackendClientConfigurationProvider)
  .getClientConfigurationAsync()
  .then((clientConfig) => {
    defaultConfig = { ...defaultConfig, ...clientConfig };
  });

const scenarioDefPromise = container
  .get<IScenarioDefinitionProvider>(TYPES.BackendScenarioDefinitionProvider)
  .getScenarioDefinition()
  .then((scenarioDef) => {
    defaultScenario = scenarioDef;
  });

const scenarioParamsPromise = container
  .get<IScenarioParameterProvider>(TYPES.BackendScenarioParameterProvider)
  .getScenarioParameters()
  .then((scenarioParams) => {
    defaultParameters = scenarioParams;
  });

const applicationActions = container
  .get<IApplicationActionProvider>(TYPES.ApplicationActionProvider)
  .getApplicationActions();

const navigationItems = container.get<INavigationItemProvider>(TYPES.NavigationItemProvider).getNavigationItems();

Promise.all([clientConfigPromise, scenarioDefPromise, scenarioParamsPromise]).finally(() => {
  store.replaceState({
    ...store.state,
    ...defaultConfig,
    ...new ParameterSelection(defaultScenario.toWrapperList(), defaultParameters.toWrapperList()),
    ...{ applicationActions, navigationItems },
  });
  const vuetify = GetVuetify(defaultConfig);
  new Vue({
    vuetify,
    router,
    store,
    // eslint-disable-next-line @typescript-eslint/explicit-function-return-type
    render: (h) => h(App),
  }).$mount('#app');
});
