import { GetterTree } from 'vuex';
import IRootState from '@/interfaces/store/IRootState';

const runSettingsGetters: GetterTree<IRootState, IRootState> = {
  canRun: (state) => {
    return state.scenarioDefinition.allParametersValid() && state.scenarioParameters.allParametersValid();
  },

  hasResults: (state) => {
    return state.currentJob.results.length > 0;
  },
};

export default runSettingsGetters;
