import { MutationTree } from 'vuex';
import IRootState from '@/interfaces/store/IRootState';

const clientConfigurationMutations: MutationTree<IRootState> = {
  // eslint-disable-next-line @typescript-eslint/no-unused-vars
  exampleClientConfiguration(state) {
    // console.log(state);
  },
};

export default clientConfigurationMutations;
