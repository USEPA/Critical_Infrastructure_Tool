import { UserVuetifyPreset } from 'vuetify';
import IVuetifyThemeSettings from './IVuetifyThemeSettings';

export default interface IClientConfiguration extends IVuetifyThemeSettings {
  theme: Partial<UserVuetifyPreset>;
  applicationTitle: string;
  applicationVersion: string;
  applicationAcronym: string;
  publisherName: string;
  applicationSponsor: string;
}
