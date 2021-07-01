import 'reflect-metadata';
import { injectable } from 'inversify';
import IApplicationActionProvider from '@/interfaces/providers/IApplicationActionProvider';
import IApplicationAction from '@/interfaces/configuration/IApplicationAction';

@injectable()
export default class DefaultApplicationActionProvider implements IApplicationActionProvider {
  // eslint-disable-next-line class-methods-use-this
  getApplicationActions(): IApplicationAction[] {
    return [
      {
        title: 'Load Scenario',
        // eslint-disable-next-line @typescript-eslint/no-empty-function
        onSelected: () => {},
        enabled: true,
        icon: 'fa-upload',
      },
      {
        title: 'Load Parameters',
        // eslint-disable-next-line @typescript-eslint/no-empty-function
        onSelected: () => {},
        enabled: true,
        icon: 'fa-upload',
      },
      {
        title: 'Save Scenario',
        // eslint-disable-next-line @typescript-eslint/no-empty-function
        onSelected: () => {},
        enabled: true,
        icon: 'fa-save',
      },
      {
        title: 'Save Parameters',
        // eslint-disable-next-line @typescript-eslint/no-empty-function
        onSelected: () => {},
        enabled: true,
        icon: 'fa-save',
      },
      {
        title: 'Save Results',
        // eslint-disable-next-line @typescript-eslint/no-empty-function
        onSelected: () => {},
        enabled: false,
        icon: 'fa-save',
      },
    ];
  }
}
