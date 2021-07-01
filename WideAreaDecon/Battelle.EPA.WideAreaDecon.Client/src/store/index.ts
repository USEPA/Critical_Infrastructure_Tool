/* eslint-disable @typescript-eslint/explicit-function-return-type */
import Vue from 'vue';
import Vuex, { StoreOptions } from 'vuex';
import IRootState from '@/interfaces/store/IRootState';
import RunSettings from './runSettings/RunSettings';
import AppSettings from './appSettings/AppSettings';
import ClientConfiguration from './clientConfiguration/ClientConfiguration';
import appSettingsMutations from './appSettings/mutations';
import clientConfigurationMutations from './clientConfiguration/mutations';
import runSettingsMutations from './runSettings/mutations';
import runSettingsGetters from './runSettings/getters';
import runSettingsActions from './runSettings/actions';
import NavigationSettings from './navigationSettings/NavigationSettings';
import navigationSettingsMutations from './navigationSettings/mutations';
import parameterSelectionMutations from './parameterSelection/mutations';
import parameterSelectionActions from './parameterSelection/actions';
import ParameterSelection from './parameterSelection/ParameterSelection';
import CurrentJob from './jobs/CurrentJob';
import currentJobMutations from './jobs/mutations';
import jobRequestActions from './jobs/actions';

Vue.use(Vuex);

const store: StoreOptions<IRootState> = {
  state: {
    ...new ClientConfiguration(),
    ...new AppSettings(),
    ...new RunSettings(),
    ...new ParameterSelection(),
    ...new NavigationSettings(),
    ...new CurrentJob(),
  },
  modules: {},
  getters: {
    ...runSettingsGetters,
  },
  mutations: {
    ...appSettingsMutations,
    ...clientConfigurationMutations,
    ...runSettingsMutations,
    ...parameterSelectionMutations,
    ...navigationSettingsMutations,
    ...currentJobMutations,
  },
  actions: {
    ...parameterSelectionActions,
    ...runSettingsActions,
    ...jobRequestActions,
  },
};

export default new Vuex.Store<IRootState>(store);
