import { ContainerModule, interfaces } from 'inversify';
import 'reflect-metadata';
import IParameterConverter from '@/interfaces/parameter/IParameterConverter';
import ParameterConverter from '@/implementations/parameter/converters/ParameterConverter';
import PROVIDER_TYPES from './converters.types';

const providersContainerModule = new ContainerModule((bind: interfaces.Bind) => {
  bind<IParameterConverter>(PROVIDER_TYPES.ParameterConverter).to(ParameterConverter);
});

export default providersContainerModule;
