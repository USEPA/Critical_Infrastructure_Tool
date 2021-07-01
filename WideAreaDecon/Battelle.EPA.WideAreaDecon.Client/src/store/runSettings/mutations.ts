import { MutationTree } from 'vuex';
import IRootState from '@/interfaces/store/IRootState';

const runSettingsMutations: MutationTree<IRootState> = {
  updateRunState(state, newState: boolean): void {
    state.runSettings.canRun = newState;
  },

  updateHasResults(state, newState: boolean): void {
    state.runSettings.hasResults = newState;
  },

  updateRepeatRun(state, newState: boolean): void {
    state.runSettings.repeatRun = newState;
  },
};

export default runSettingsMutations;
