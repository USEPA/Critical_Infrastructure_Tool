import IHomeOptionAction from '@/interfaces/configuration/IHomeOptionAction';

export default class HomeOptionRouterAction implements IHomeOptionAction {
  nextRouteName: string;

  // eslint-disable-next-line class-methods-use-this
  isModal(): boolean {
    return false;
  }

  getNext(): string {
    return this.nextRouteName;
  }

  constructor(nextRouteName: string) {
    this.nextRouteName = nextRouteName;
  }
}
