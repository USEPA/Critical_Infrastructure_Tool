import IHomeOptionAction from './IHomeOptionAction';

export default interface IHomeOptions {
  title: string;
  image: string;
  helpMessage: string;
  helpActive: boolean;
  action: IHomeOptionAction;
}
