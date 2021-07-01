import IClientConfiguration from '@/interfaces/configuration/IClientConfiguration';
import { UserVuetifyPreset } from 'vuetify';

export default class ClientConfiguration implements IClientConfiguration {
  theme: Partial<UserVuetifyPreset> = {};

  applicationTitle = 'unknown';

  applicationVersion = 'unknown';

  publisherName = 'unknown';

  applicationAcronym = 'UNK';

  applicationSponsor = 'unkown';
}
