import IHomeOptions from '@/interfaces/configuration/IHomeOptions';
import IHomeOptionAction from '@/interfaces/configuration/IHomeOptionAction';

export default class HomeOptions implements IHomeOptions {
  title: string;

  image: string;

  helpMessage: string;

  helpActive: boolean;

  action: IHomeOptionAction;

  constructor(title: string, image: string, helpMessage: string, action: IHomeOptionAction) {
    this.title = title;
    this.image = image;
    this.helpMessage = helpMessage;
    this.helpActive = false;
    this.action = action;
  }
}
