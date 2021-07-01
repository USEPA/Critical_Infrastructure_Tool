import INavigationItem from '../configuration/INavigationItem';

export default interface INavigationItemProvider {
  getNavigationItems(): INavigationItem[];
}
