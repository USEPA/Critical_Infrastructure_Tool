import 'reflect-metadata';
import { injectable } from 'inversify';
import INavigationItemProvider from '@/interfaces/providers/INavigationItemProvider';
import INavigationItem from '@/interfaces/configuration/INavigationItem';
import store from '@/store';
import NavigationItem from '../configuration/NavigationItem';

@injectable()
export default class DefaultNavigationItemProvider implements INavigationItemProvider {
  // eslint-disable-next-line class-methods-use-this
  getNavigationItems(): INavigationItem[] {
    return [
      new NavigationItem(
        'Define Scenario',
        'fa-biohazard',
        '/DefineScenario',
        true,
        {
          enabled: 'Parameters which construct the contamination scenario',
          disabled: 'ERROR - scenario definition should always be enabled',
        },
        () => {
          return store.state.scenarioDefinition.numberInvalidParameters();
        },
      ),
      new NavigationItem(
        'Modify Parameters',
        'fa-shower',
        '/ModifyParameters',
        true,
        {
          enabled: 'Parameters which define costs and efficacy of decontamination efforts',
          disabled: 'ERROR - modify parameters should always be enabled',
        },
        () => {
          return store.state.scenarioParameters.numberInvalidParameters();
        },
      ),
      new NavigationItem(
        'View Results',
        'fa-building',
        '/ViewResults',
        false,
        {
          enabled: 'View the results from the latest model run',
          disabled: 'No results - run model to generate results...',
        },
        () => {
          return 0;
        },
      ),
    ];
  }
}
