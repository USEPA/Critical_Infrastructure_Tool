import { MutationTree } from 'vuex';
import IRootState from '@/interfaces/store/IRootState';
import INavigationItem from '@/interfaces/configuration/INavigationItem';

const appSettingsMutations: MutationTree<IRootState> = {
  // eslint-disable-next-line @typescript-eslint/no-empty-function, @typescript-eslint/no-unused-vars
  exampleAppSettingsMutations(state) {},

  setNavigationItems(state, newState: INavigationItem[]): void {
    state.navigationItems = newState;
  },
};

export default appSettingsMutations;
