import ITooltipSelector from './ITooltipSelector';

export default interface INavigationItem {
  title: string;
  icon: string;
  link: string;
  enabled: boolean;
  tooltip: ITooltipSelector;

  getNumberInvalid(): number;
}
