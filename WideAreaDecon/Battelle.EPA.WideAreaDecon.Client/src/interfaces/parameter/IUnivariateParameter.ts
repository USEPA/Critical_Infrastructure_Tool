import Distribution from 'battelle-common-typescript-statistics';
import IParameter from './IParameter';

export default interface IUnivariateParameter extends IParameter {
  min?: number;
  max?: number;
  mean?: number;
  mode?: number;
  stdDev?: number;
  text?: string;
  distribution?: Distribution;
}
