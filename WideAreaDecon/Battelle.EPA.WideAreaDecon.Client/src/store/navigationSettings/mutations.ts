import { MutationTree } from 'vuex';
import IRootState from '@/interfaces/store/IRootState';

const navigationSettingsMutations: MutationTree<IRootState> = {
  enableNavigationTabs(state: IRootState) {
    state.enableNavigationTabs = true;
  },

  disableNavigationTabs(state: IRootState) {
    state.enableNavigationTabs = false;
  },
};

export default navigationSettingsMutations;
