import INavigationItem from '@/interfaces/configuration/INavigationItem';
import ITooltipSelector from '@/interfaces/configuration/ITooltipSelector';

export default class NavigationItem implements INavigationItem {
  title: string;

  icon: string;

  link: string;

  enabled: boolean;

  tooltip: ITooltipSelector;

  // eslint-disable-next-line class-methods-use-this
  getNumberInvalid(): number {
    return 0;
  }

  constructor(
    title: string,
    icon: string,
    link: string,
    enabled: boolean,
    tooltip: ITooltipSelector,
    getNumberInvalid: () => number,
  ) {
    this.title = title;
    this.icon = icon;
    this.link = link;
    this.enabled = enabled;
    this.tooltip = tooltip;
    this.getNumberInvalid = getNumberInvalid;
  }
}
