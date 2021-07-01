import ParameterType from '@/enums/parameter/parameterType';

const changeableDistributionTypes = new Array<ParameterType>(
  ParameterType.constant,
  ParameterType.uniform,
  ParameterType.pert,
  ParameterType.truncatedNormal,
  ParameterType.truncatedLogNormal,
  ParameterType.logNormal,
  ParameterType.logUniform,
  ParameterType.truncatedLogNormal,
  ParameterType.weibull,
  ParameterType.bimodalTruncatedNormal,
  ParameterType.textValue,
);

// eslint-disable-next-line import/prefer-default-export
export { changeableDistributionTypes };
