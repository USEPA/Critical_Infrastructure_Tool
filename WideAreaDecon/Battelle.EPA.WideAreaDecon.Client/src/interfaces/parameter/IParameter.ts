import ParameterType from '@/enums/parameter/parameterType';
import ParameterMetaData from '@/implementations/parameter/ParameterMetaData';

export default interface IParameter {
  type: ParameterType;

  isSet: boolean;

  isEquivalent(other: IParameter): boolean;

  metaData: ParameterMetaData;
}
