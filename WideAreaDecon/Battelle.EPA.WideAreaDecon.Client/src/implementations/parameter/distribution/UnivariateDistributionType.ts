import ParameterType from '@/enums/parameter/parameterType';
import IParameter from '@/interfaces/parameter/IParameter';
import BetaPERT from './BetaPERT';
import Constant from './Constant';
import LogUniform from './LogUniform';
import TruncatedNormal from './TruncatedNormal';
import TruncatedLogNormal from './TruncatedLogNormal';
import Uniform from './Uniform';
import BimodalTruncatedNormal from './BimodalTruncatedNormal';
import LogNormal from './LogNormal';
import Weibull from './Weibull';
import TextValue from './TextValue';

type UnivariateDistributionType =
  | BetaPERT
  | BimodalTruncatedNormal
  | Constant
  | LogNormal
  | LogUniform
  | TruncatedLogNormal
  | TruncatedNormal
  | Uniform
  | Weibull
  | TextValue;

function isUnivariateDistribution(param: IParameter): boolean {
  switch (param.type) {
    case ParameterType.bimodalTruncatedNormal:
    case ParameterType.constant:
    case ParameterType.logNormal:
    case ParameterType.logUniform:
    case ParameterType.pert:
    case ParameterType.truncatedLogNormal:
    case ParameterType.truncatedNormal:
    case ParameterType.uniform:
    case ParameterType.uniformXDependent:
    case ParameterType.textValue:
    case ParameterType.weibull:
      return true;
    case ParameterType.null:
    default:
      throw new Error('Unrecognized Parameter Type');
  }
}

export default UnivariateDistributionType;

export { isUnivariateDistribution };
