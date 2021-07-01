import IHomeOptionAction from '@/interfaces/configuration/IHomeOptionAction';

export default class HomeOptionModalAction implements IHomeOptionAction {
  nextPageName: string;

  // eslint-disable-next-line class-methods-use-this
  isModal(): boolean {
    return true;
  }

  getNext(): string {
    return this.nextPageName;
  }

  constructor(nextPageName: string) {
    this.nextPageName = nextPageName;
  }
}
