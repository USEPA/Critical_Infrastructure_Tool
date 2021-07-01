import IAppSettings from '@/interfaces/store/appSettings/IAppSettings';
import { UserVuetifyPreset } from 'vuetify';
import INavigationItem from '@/interfaces/configuration/INavigationItem';
import IApplicationAction from '@/interfaces/configuration/IApplicationAction';
import IRunSettings from '@/interfaces/store/runSettings/IRunSettings';
import IClientConfiguration from '@/interfaces/configuration/IClientConfiguration';
import RunSettings from '../runSettings/RunSettings';

export default class AppSettings implements IAppSettings {
  theme: Partial<UserVuetifyPreset> = {};

  applicationTitle = 'unknown';

  applicationVersion = 'unknown';

  publisherName = 'unknown';

  errorIcon = 'fa-exclamation-triangle';

  navigationItems: INavigationItem[] = [];

  applicationActions: IApplicationAction[] = [];

  runSettings: IRunSettings = new RunSettings();

  // eslint-disable-next-line @typescript-eslint/explicit-module-boundary-types
  updateSettings(other: IClientConfiguration) {
    this.applicationTitle = other.applicationTitle;
    this.applicationVersion = other.applicationVersion;
    this.publisherName = other.publisherName;
    this.theme = other.theme;
  }
}
