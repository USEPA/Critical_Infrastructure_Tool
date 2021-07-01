import IApplicationAction from '../configuration/IApplicationAction';

export default interface IApplicationActionProvider {
  getApplicationActions(): IApplicationAction[];
}
