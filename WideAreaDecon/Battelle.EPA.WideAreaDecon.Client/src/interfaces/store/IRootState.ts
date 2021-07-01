import IRunSettings from './runSettings/IRunSettings';
import IAppSettings from './appSettings/IAppSettings';
import IClientConfiguration from '../configuration/IClientConfiguration';
import INavigationSettings from './navigationSettings/INavigationSettings';
import IParameterSelection from './parameterSelection/IParameterSelection';
import ICurrentJob from './jobs/ICurrentJob';

export default interface IRootState
  extends IClientConfiguration,
    IAppSettings,
    IRunSettings,
    IParameterSelection,
    INavigationSettings,
    ICurrentJob {}
