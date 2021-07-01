import { ActionTree } from 'vuex';
import IRootState from '@/interfaces/store/IRootState';

const runSettingsActions: ActionTree<IRootState, IRootState> = {
  setRepeatRun: ({ commit }, newValue) => {
    commit('updateRepeatRun', newValue);
  },
};

export default runSettingsActions;
