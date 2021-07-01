export default interface IApplicationAction {
  title: string;
  onSelected(): void;
  enabled: boolean;
  icon: string;
}
