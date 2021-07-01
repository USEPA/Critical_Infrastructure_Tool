import IRunSettings from '@/interfaces/store/runSettings/IRunSettings';

export default class RunSettings implements IRunSettings {
  canRun = false;

  hasResults = false;

  repeatRun = false;
}
