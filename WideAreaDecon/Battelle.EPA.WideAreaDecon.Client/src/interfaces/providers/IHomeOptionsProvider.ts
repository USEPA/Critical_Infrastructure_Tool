import IHomeOptions from '../configuration/IHomeOptions';

export default interface IHomeOptionsProvider {
  getOptions(): IHomeOptions[];
}
