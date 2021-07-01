import ParameterWrapperList from '@/implementations/parameter/ParameterWrapperList';
import IRootState from '@/interfaces/store/IRootState';
import { ActionTree } from 'vuex';

const parameterSelectionActions: ActionTree<IRootState, IRootState> = {
  setScenarioDefinition({ commit }, newDefinition: ParameterWrapperList): void {
    commit('setScenarioDefinition', newDefinition);
  },
  setScenarioParameters({ commit }, newParameters: ParameterWrapperList): void {
    commit('setScenarioParameters', newParameters);
  },
};

export default parameterSelectionActions;
