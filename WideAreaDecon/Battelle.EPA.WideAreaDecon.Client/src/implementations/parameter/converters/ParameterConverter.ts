/* eslint-disable class-methods-use-this */
import IParameterConverter from '@/interfaces/parameter/IParameterConverter';
import IParameter from '@/interfaces/parameter/IParameter';
import ParameterType from '@/enums/parameter/parameterType';
import * as Utility from '@/mixin/mathUtilityMixin';
import { nelderMead } from '@/mixin/solverMixin';
import { injectable } from 'inversify';
import Uniform from '../distribution/Uniform';
import TruncatedNormal from '../distribution/TruncatedNormal';
import TruncatedLogNormal from '../distribution/TruncatedLogNormal';
import BetaPERT from '../distribution/BetaPERT';
import LogUniform from '../distribution/LogUniform';
import Constant from '../distribution/Constant';
import { isUnivariateDistribution } from '../distribution/UnivariateDistributionType';
import IUnivariateParameter from '../../../interfaces/parameter/IUnivariateParameter';
import BimodalTruncatedNormal from '../distribution/BimodalTruncatedNormal';
import LogNormal from '../distribution/LogNormal';
import NullParameter from '../NullParameter';
import UniformXDependent from '../distribution/UniformXDependent';
import Weibull from '../distribution/Weibull';
import TextValue from '../distribution/TextValue';
import ParameterMetaData from '../ParameterMetaData';
import EnumeratedFraction from '../list/enumeratedFraction';
import EnumeratedParameter from '../list/enumeratedParameter';

@injectable()
export default class ParameterConverter implements IParameterConverter {
  convertToNewType(old: IParameter, newType: ParameterType): IParameter {
    if (old.type === newType) {
      return old;
    }
    return isUnivariateDistribution(old)
      ? this.convertFromUnivariate(<IUnivariateParameter>old, newType)
      : this.convertFromNonUnivariate(old, newType);
  }

  convertFromUnivariate(old: IUnivariateParameter, newType: ParameterType): IParameter {
    switch (newType) {
      case ParameterType.bimodalTruncatedNormal:
        return new BimodalTruncatedNormal(old.metaData, old.mean, old.stdDev, old.mean, old.stdDev, old.min, old.max);
      case ParameterType.constant:
        return new Constant(old.metaData, old.mean);
      case ParameterType.logNormal:
        return new LogNormal(old.metaData, old.mean, old.stdDev);
      case ParameterType.logUniform:
        return new LogUniform(old.metaData, Utility.convertToLog10(old.min), Utility.convertToLog10(old.max));
      case ParameterType.null:
        return new NullParameter();
      case ParameterType.pert:
        return new BetaPERT(old.metaData, old.min, old.max, old.mode);
      case ParameterType.truncatedLogNormal:
        return new TruncatedLogNormal(
          old.metaData,
          Utility.convertToLog10(old.min),
          Utility.convertToLog10(old.max),
          Utility.convertToLog10(old.mean),
          Utility.convertToLog10(old.stdDev),
        );
      case ParameterType.truncatedNormal:
        return new TruncatedNormal(old.metaData, old.min, old.max, old.mean, old.stdDev);
      case ParameterType.uniform:
        return new Uniform(old.metaData, old.min, old.max);
      case ParameterType.uniformXDependent:
        return new UniformXDependent(old.metaData);
      case ParameterType.textValue:
        return new TextValue(old.metaData, old.text || 'null');
      case ParameterType.weibull: {
        if (old.mean === undefined || old.stdDev === undefined) {
          return new Weibull(old.metaData);
        }

        const actMean = old.mean;
        const actVar = old.stdDev ** 2;
        const minimize = (values: number[]): number => {
          const actual = new Weibull(new ParameterMetaData(), values[0], values[1]);

          if (!!actual.mean && !!actual.variance) {
            return Math.sqrt((actual.mean - actMean) ** 2 + (actual.variance - actVar ** 2) ** 2);
          }
          return Infinity;
        };
        const guess = [1, 1];

        // SUT
        const sln = nelderMead(minimize, guess);
        return new Weibull(old.metaData, sln.Input[0], sln.Input[1]);
      }
      case ParameterType.enumeratedFraction:
      case ParameterType.enumeratedParameter:
      default:
        throw new Error('Cannot convert to requested type');
    }
  }

  convertFromNonUnivariate(old: IParameter, newType: ParameterType): IParameter {
    switch (newType) {
      case ParameterType.bimodalTruncatedNormal:
        return new BimodalTruncatedNormal(old.metaData);
      case ParameterType.constant:
        return new Constant(old.metaData);
      case ParameterType.logNormal:
        return new LogNormal(old.metaData);
      case ParameterType.logUniform:
        return new LogUniform(old.metaData);
      case ParameterType.null:
        return new NullParameter();
      case ParameterType.pert:
        return new BetaPERT(old.metaData);
      case ParameterType.truncatedLogNormal:
        return new TruncatedLogNormal(old.metaData);
      case ParameterType.truncatedNormal:
        return new TruncatedNormal(old.metaData);
      case ParameterType.uniform:
        return new Uniform(old.metaData);
      case ParameterType.uniformXDependent:
        return new UniformXDependent(old.metaData);
      case ParameterType.weibull:
        return new Weibull(old.metaData);
      case ParameterType.textValue:
        return new TextValue(old.metaData);
      case ParameterType.enumeratedFraction:
        return new EnumeratedFraction(old.metaData);
      case ParameterType.enumeratedParameter:
        return new EnumeratedParameter(old.metaData);
      default:
        throw new Error('New Type not recognized');
    }
  }
}
