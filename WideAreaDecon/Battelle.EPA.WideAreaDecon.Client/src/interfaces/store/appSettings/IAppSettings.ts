import INavigationItem from '@/interfaces/configuration/INavigationItem';
import IApplicationAction from '@/interfaces/configuration/IApplicationAction';
import IRunSettings from '../runSettings/IRunSettings';

export default interface IAppSettings {
  navigationItems: INavigationItem[];
  applicationActions: IApplicationAction[];
  runSettings: IRunSettings;
}
