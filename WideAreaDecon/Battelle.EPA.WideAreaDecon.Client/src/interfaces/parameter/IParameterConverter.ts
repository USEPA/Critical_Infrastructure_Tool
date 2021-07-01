import ParameterType from '@/enums/parameter/parameterType';
import IParameter from './IParameter';

export default interface IParameterConverter {
  convertToNewType(old: IParameter, newType: ParameterType): IParameter;
}
